#!/usr/bin/env python3
"""Validate a translation-unit handoff and return its selected context as JSON.

The checker is read-only. Paths in the handoff are resolved from the explicit
project root. It does not assume a language, work type, directory layout, or
required character.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
DISPOSITIONS = {"pending", "glossary", "unit_only"}
TYPE_NAMES = {
    type(None): "null",
    bool: "boolean",
    int: "number",
    float: "number",
    str: "string",
    list: "array",
    dict: "object",
}


def type_name(value: object) -> str:
    return TYPE_NAMES.get(type(value), type(value).__name__)


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKC", value)
    text = text.replace("’", "'")
    return " ".join(text.split()).casefold()


def resolve_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def read_utf8(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        return None, f"Not valid UTF-8 text: {path}"
    except OSError as exc:
        return None, f"Could not read {path}: {exc.strerror or exc}"


def row_cells(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def is_separator_row(line: str) -> bool:
    if not line.strip().startswith("|"):
        return False
    cells = row_cells(line)
    return bool(cells) and all(
        cell and set(cell) <= set(":-") and "-" in cell for cell in cells
    )


def parse_glossary(text: str) -> dict[str, list[str]]:
    """Read the first two columns of every Markdown table."""
    lines = text.splitlines()
    entries: dict[str, list[str]] = {}
    index = 0
    while index < len(lines):
        is_header = (
            lines[index].strip().startswith("|")
            and index + 1 < len(lines)
            and is_separator_row(lines[index + 1])
        )
        if not is_header:
            index += 1
            continue
        index += 2
        while index < len(lines) and lines[index].strip().startswith("|"):
            if not is_separator_row(lines[index]):
                cells = row_cells(lines[index])
                if len(cells) >= 2 and cells[0]:
                    entries.setdefault(normalize_text(cells[0]), []).append(cells[1])
            index += 1
    return entries


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def extract_markdown_section(text: str, requested: str) -> tuple[str | None, str | None]:
    lines = text.splitlines()
    wanted = normalize_text(requested.lstrip("#").strip())
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2)))
    matches = [item for item in headings if normalize_text(item[2]) == wanted]
    if not matches:
        return None, f"Section not found: {requested}"
    if len(matches) > 1:
        return None, f"Section is ambiguous: {requested}"
    start, level, _ = matches[0]
    end = len(lines)
    for index, next_level, _ in headings:
        if index > start and next_level <= level:
            end = index
            break
    return "\n".join(lines[start:end]).strip(), None


def base_result(status: str) -> dict[str, Any]:
    return {
        "status": status,
        "translation_unit": {},
        "source": {},
        "context": [],
        "terms": [],
        "warnings": [],
        "errors": [],
    }


def check_context(project_root: Path | str, handoff_path: Path | str) -> dict[str, Any]:
    root = Path(project_root).resolve()
    handoff = Path(handoff_path)
    if not handoff.is_absolute():
        handoff = root / handoff
    handoff = handoff.resolve()

    result = base_result("error")
    text, read_error = read_utf8(handoff)
    if read_error:
        result["errors"].append(read_error)
        return result
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        result["errors"].append(
            f"Invalid JSON in {handoff}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
        return result
    if not isinstance(data, dict):
        result["errors"].append(
            f"Handoff root must be an object, got {type_name(data)}"
        )
        return result
    if data.get("schema_version") != SCHEMA_VERSION:
        result["errors"].append(
            f"schema_version must be {SCHEMA_VERSION}"
        )

    unit = data.get("translation_unit")
    if not isinstance(unit, dict):
        result["errors"].append("translation_unit must be an object")
        unit = {}
    required_unit_fields = ("project", "id", "source_language", "target_language")
    for field in required_unit_fields:
        value = unit.get(field)
        if not isinstance(value, str) or not value.strip():
            result["errors"].append(f"translation_unit.{field} must be a non-empty string")
    result["translation_unit"] = unit

    material_complete = data.get("material_complete")
    if not isinstance(material_complete, bool):
        result["errors"].append("material_complete must be a boolean")

    source = data.get("source")
    if not isinstance(source, dict):
        result["errors"].append("source must be an object")
        source = {}
    source_value = source.get("path")
    source_path: Path | None = None
    source_text = ""
    if isinstance(source_value, str) and source_value.strip():
        source_path = resolve_path(root, source_value)
        if not source_path.is_file():
            result["errors"].append(f"Source file not found: {source_path}")
        else:
            source_text_value, source_error = read_utf8(source_path)
            if source_error:
                result["errors"].append(source_error)
            else:
                source_text = source_text_value or ""
    elif material_complete is True:
        result["errors"].append("source.path must be a non-empty string")
    result["source"] = {
        "original": source.get("original"),
        "path": str(source_path) if source_path else None,
        "verified": source.get("verified"),
    }
    if not isinstance(source.get("verified"), bool):
        result["errors"].append("source.verified must be a boolean")

    handoff_warnings = data.get("warnings", [])
    if not isinstance(handoff_warnings, list) or not all(
        isinstance(item, str) for item in handoff_warnings
    ):
        result["errors"].append("warnings must be an array of strings")
    else:
        result["warnings"].extend(item for item in handoff_warnings if item.strip())

    glossary_entries: dict[str, list[str]] = {}
    glossary_value = data.get("glossary")
    glossary_path: Path | None = None
    if glossary_value is not None:
        if not isinstance(glossary_value, str) or not glossary_value.strip():
            result["errors"].append("glossary must be null or a non-empty path string")
        else:
            glossary_path = resolve_path(root, glossary_value)
            if not glossary_path.is_file():
                result["errors"].append(f"Glossary file not found: {glossary_path}")
            else:
                glossary_text, glossary_error = read_utf8(glossary_path)
                if glossary_error:
                    result["errors"].append(glossary_error)
                else:
                    glossary_entries = parse_glossary(glossary_text or "")

    context_items = data.get("context_to_read", [])
    if not isinstance(context_items, list):
        result["errors"].append("context_to_read must be an array")
        context_items = []
    for index, item in enumerate(context_items):
        where = f"context_to_read[{index}]"
        if not isinstance(item, dict):
            result["errors"].append(f"{where} must be an object")
            continue
        path_value = item.get("path")
        if not isinstance(path_value, str) or not path_value.strip():
            result["errors"].append(f"{where}.path must be a non-empty string")
            continue
        path = resolve_path(root, path_value)
        content, context_error = read_utf8(path)
        if context_error:
            result["errors"].append(context_error)
            continue
        section = item.get("section")
        selected = content or ""
        if section is not None:
            if not isinstance(section, str) or not section.strip():
                result["errors"].append(f"{where}.section must be a non-empty string or null")
                continue
            selected, section_error = extract_markdown_section(content or "", section)
            if section_error:
                result["errors"].append(f"{path}: {section_error}")
                continue
        result["context"].append(
            {
                "role": item.get("role", "reference"),
                "path": str(path),
                "section": section,
                "content": selected,
            }
        )

    terms = data.get("terms", [])
    if not isinstance(terms, list):
        result["errors"].append("terms must be an array")
        terms = []
    pending = False
    source_lines = source_text.splitlines()
    for index, item in enumerate(terms):
        where = f"terms[{index}]"
        if not isinstance(item, dict):
            result["errors"].append(f"{where} must be an object")
            continue
        source_term = item.get("source")
        disposition = item.get("disposition")
        target_term = item.get("target")
        if not isinstance(source_term, str) or not source_term.strip():
            result["errors"].append(f"{where}.source must be a non-empty string")
            continue
        if disposition not in DISPOSITIONS:
            result["errors"].append(
                f"{where}.disposition must be one of {sorted(DISPOSITIONS)}"
            )
            continue
        if disposition in {"glossary", "unit_only"} and (
            not isinstance(target_term, str) or not target_term.strip()
        ):
            result["errors"].append(
                f"{where}.target must be a non-empty string for {disposition}"
            )
            continue
        key = normalize_text(source_term)
        occurrences = [
            {"line": number, "text": line}
            for number, line in enumerate(source_lines, start=1)
            if key in normalize_text(line)
        ]
        if source_text and not occurrences:
            result["warnings"].append(f"Term not found in source: {source_term}")
        glossary_status = "not_required"
        if disposition == "pending":
            pending = True
            glossary_status = "pending"
        elif disposition == "glossary":
            glossary_status = "missing"
            candidates = glossary_entries.get(key, [])
            if glossary_path is None:
                result["errors"].append(
                    f"{where} requires a glossary path"
                )
            elif not candidates:
                result["errors"].append(
                    f"Glossary entry not found for: {source_term}"
                )
            elif normalize_text(target_term) not in {
                normalize_text(candidate) for candidate in candidates
            }:
                result["errors"].append(
                    f"Glossary target mismatch for {source_term}: expected {target_term!r}"
                )
            else:
                glossary_status = "present"
        result["terms"].append(
            {
                "source": source_term,
                "target": target_term,
                "disposition": disposition,
                "glossary_status": glossary_status,
                "occurrences": occurrences,
            }
        )

    if result["errors"]:
        result["status"] = "error"
    elif material_complete is False or source.get("verified") is False:
        result["status"] = "material_incomplete"
    elif pending:
        result["status"] = "terms_pending"
    else:
        result["status"] = "ready"
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
        description="Validate a translation context handoff and print JSON. Read-only."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root used to resolve relative paths (default: current directory)",
    )
    parser.add_argument(
        "--handoff",
        required=True,
        help="Path to sourcing-handoff.json, relative to the project root or absolute",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = build_parser().parse_args(argv)
    try:
        result = check_context(args.project_root, args.handoff)
    except Exception as exc:  # Keep the CLI JSON-only on unexpected failures.
        result = base_result("error")
        result["errors"].append(f"Unexpected checker failure: {type(exc).__name__}: {exc}")
    emit(result)
    return 1 if result["status"] == "error" else 0


if __name__ == "__main__":
    raise SystemExit(main())
