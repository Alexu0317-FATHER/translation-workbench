#!/usr/bin/env python3
"""Check deterministic entry and completion conditions for workflow stages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from check_translation_context import check_context


STAGES = ("translation", "independent-review", "review-complete", "finalization")
REVIEW_HASH_RE = re.compile(
    r"<!--\s*translation-workbench:draft-sha256-(before|after)=([0-9a-fA-F]{64})\s*-->"
)


def resolve_path(project_root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def review_hashes(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    return {position: value.casefold() for position, value in REVIEW_HASH_RE.findall(text)}


def result_base(stage: str) -> dict[str, Any]:
    return {
        "status": "ready",
        "stage": stage,
        "checks": [],
        "context_status": None,
        "draft_sha256": None,
        "errors": [],
    }


def add_check(result: dict[str, Any], name: str, ok: bool, detail: str) -> None:
    result["checks"].append({"name": name, "ok": ok, "detail": detail})
    if not ok and result["status"] != "error":
        result["status"] = "blocked"


def require_file(
    result: dict[str, Any], project_root: Path, value: str | None, label: str
) -> Path | None:
    if not value:
        add_check(result, label, False, f"No path supplied for {label}")
        return None
    path = resolve_path(project_root, value)
    assert path is not None
    if not path.is_file():
        add_check(result, label, False, f"File not found: {path}")
        return None
    if path.stat().st_size == 0:
        add_check(result, label, False, f"File is empty: {path}")
        return None
    add_check(result, label, True, str(path))
    return path


def check_stage(
    stage: str,
    project_root: Path | str,
    handoff: str | None = None,
    translation: str | None = None,
    drafting_notes: str | None = None,
    review_notes: str | None = None,
    expected_draft_sha256: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    result = result_base(stage)
    if stage not in STAGES:
        result["status"] = "error"
        result["errors"].append(f"Unknown stage: {stage}")
        return result

    if stage in {"translation", "independent-review", "finalization"}:
        if not handoff:
            add_check(result, "context handoff", False, "No handoff path supplied")
        else:
            context_result = check_context(root, handoff)
            result["context_status"] = context_result["status"]
            if context_result["status"] == "error":
                result["status"] = "error"
                result["errors"].extend(context_result["errors"])
                add_check(result, "context handoff", False, "Context checker returned error")
            elif context_result["status"] != "ready":
                add_check(
                    result,
                    "context handoff",
                    False,
                    f"Context status is {context_result['status']}",
                )
            elif context_result["warnings"]:
                add_check(
                    result,
                    "context handoff",
                    False,
                    "Context warnings must be resolved: " + "; ".join(context_result["warnings"]),
                )
            else:
                add_check(result, "context handoff", True, "Context is ready")

    if stage == "translation":
        return result

    translation_path = require_file(result, root, translation, "translation draft")
    if translation_path is not None:
        result["draft_sha256"] = sha256_file(translation_path)

    if stage == "independent-review":
        if review_notes:
            review_path = resolve_path(root, review_notes)
            assert review_path is not None
            if review_path.exists():
                add_check(
                    result,
                    "review output",
                    False,
                    f"Review file already exists and must not be overwritten: {review_path}",
                )
            else:
                add_check(result, "review output", True, str(review_path))
        else:
            add_check(result, "review output", False, "No review-notes output path supplied")
        return result

    if stage == "review-complete":
        require_file(result, root, review_notes, "review notes")
        if not expected_draft_sha256:
            add_check(
                result,
                "draft checksum",
                False,
                "No expected draft SHA-256 supplied",
            )
        elif translation_path is not None:
            actual = result["draft_sha256"]
            add_check(
                result,
                "draft checksum",
                actual.casefold() == expected_draft_sha256.casefold(),
                f"expected={expected_draft_sha256} actual={actual}",
            )
        return result

    require_file(result, root, drafting_notes, "drafting notes")
    review_path = require_file(result, root, review_notes, "review notes")
    if review_path is not None and translation_path is not None:
        try:
            hashes = review_hashes(review_path)
        except UnicodeDecodeError:
            result["status"] = "error"
            result["errors"].append(f"Review notes are not valid UTF-8: {review_path}")
            return result
        before = hashes.get("before")
        after = hashes.get("after")
        actual = result["draft_sha256"]
        if before is None or after is None:
            add_check(
                result,
                "review draft checksum record",
                False,
                "Review notes do not contain both translation-workbench draft checksum markers",
            )
        else:
            add_check(
                result,
                "review draft checksum record",
                before == after == actual,
                f"before={before} after={after} current={actual}",
            )
    return result


def emit(result: dict[str, Any]) -> None:
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    sys.stdout.buffer.write(payload.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check deterministic translation workflow stage conditions."
    )
    parser.add_argument("stage", choices=STAGES)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--handoff")
    parser.add_argument("--translation")
    parser.add_argument("--drafting-notes")
    parser.add_argument("--review-notes")
    parser.add_argument("--expected-draft-sha256")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = build_parser().parse_args(argv)
    try:
        result = check_stage(
            stage=args.stage,
            project_root=args.project_root,
            handoff=args.handoff,
            translation=args.translation,
            drafting_notes=args.drafting_notes,
            review_notes=args.review_notes,
            expected_draft_sha256=args.expected_draft_sha256,
        )
    except Exception as exc:  # Keep the CLI JSON-only on unexpected failures.
        result = result_base(args.stage)
        result["status"] = "error"
        result["errors"].append(f"Unexpected checker failure: {type(exc).__name__}: {exc}")
    emit(result)
    return 0 if result["status"] == "ready" else 1 if result["status"] == "error" else 2


if __name__ == "__main__":
    raise SystemExit(main())
