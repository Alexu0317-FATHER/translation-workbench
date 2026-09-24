#!/usr/bin/env python3
"""Check deterministic entry and completion conditions for workflow stages."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from check_translation_context import check_context


STAGES = ("translation", "finalization")


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
    initial_draft: str | None = None,
    drafting_notes: str | None = None,
    review_notes: str | None = None,
    resume: bool = False,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    result = result_base(stage)
    if stage not in STAGES:
        result["status"] = "error"
        result["errors"].append(f"Unknown stage: {stage}")
        return result

    if stage in {"translation", "finalization"}:
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

    require_file(result, root, drafting_notes, "drafting notes")
    snapshot_path = require_file(result, root, initial_draft, "initial draft snapshot")
    if snapshot_path is not None and translation_path is not None:
        distinct = snapshot_path != translation_path
        add_check(result, "snapshot is separate", distinct, "Snapshot must be a separate file")
        if distinct and not resume:
            snapshot_hash = sha256_file(snapshot_path)
            add_check(
                result,
                "initial draft unchanged",
                snapshot_hash == result["draft_sha256"],
                f"snapshot={snapshot_hash} current={result['draft_sha256']}",
            )

    if not review_notes:
        add_check(result, "finalization record", False, "No review-notes path supplied")
    else:
        review_path = resolve_path(root, review_notes)
        assert review_path is not None
        if resume:
            require_file(result, root, review_notes, "finalization record")
        else:
            add_check(
                result,
                "finalization record",
                not review_path.exists(),
                f"Review notes already exist: {review_path}"
                if review_path.exists()
                else str(review_path),
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
    parser.add_argument("--initial-draft")
    parser.add_argument("--drafting-notes")
    parser.add_argument("--review-notes")
    parser.add_argument("--resume", action="store_true")
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
            initial_draft=args.initial_draft,
            drafting_notes=args.drafting_notes,
            review_notes=args.review_notes,
            resume=args.resume,
        )
    except Exception as exc:  # Keep the CLI JSON-only on unexpected failures.
        result = result_base(args.stage)
        result["status"] = "error"
        result["errors"].append(f"Unexpected checker failure: {type(exc).__name__}: {exc}")
    emit(result)
    return 0 if result["status"] == "ready" else 1 if result["status"] == "error" else 2


if __name__ == "__main__":
    raise SystemExit(main())
