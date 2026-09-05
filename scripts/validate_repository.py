#!/usr/bin/env python3
"""Validate the public Translation Workbench repository with standard Python."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "translation-workbench"
SKILL_FILE = SKILL / "SKILL.md"
REQUIRED = (
    "../../LICENSE",
    "../../README.zh.md",
    "SKILL.md",
    "agents/openai.yaml",
    "references/project-initialization.md",
    "references/sourcing.md",
    "references/translation.md",
    "references/independent-review.md",
    "references/finalization.md",
    "scripts/check_translation_context.py",
    "scripts/check_stage.py",
    "scripts/test_check_translation_context.py",
    "scripts/test_check_stage.py",
    "assets/templates/project-readme.md",
    "assets/templates/sourcing-handoff.json",
    "assets/templates/glossary.md",
    "assets/templates/character-profiles.md",
    "assets/templates/background-notes.md",
    "assets/templates/translator-style.md",
    "assets/templates/sources.md",
    "assets/templates/drafting-notes.md",
    "assets/templates/review-notes.md",
)

MARKDOWN_LINK_RE = re.compile(r"\]\(([^)]+)\)")
HTML_REFERENCE_RE = re.compile(r'(?i)(?:href|src)\s*=\s*["\']([^"\']+)["\']')
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
PRIVATE_PATH_RE = re.compile(r"(?i)(?:^|[\s('`\"])[a-z]:\\")
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
TOKEN_RE = re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})\b")
UNFINISHED_RE = re.compile("(?i)\\[" + "TODO|\\b" + "FIX" + "ME\\b")
SEMVER_RE = re.compile(r"\A\d+\.\d+\.\d+\Z")
VERSION_CITATIONS = (
    ("README.md", re.compile(r"(?m)^Current version: `([^`]+)`\s*$")),
    ("README.zh.md", re.compile(r"(?m)^当前版本：`([^`]+)`\s*$")),
)
LEGACY_TERMS = (
    "Vermin" + "tide",
    "Fat" + "shark",
    "franz-" + "lohners",
    "Lexi" + "canum",
    "Content_" + "Creator",
    "QQ" + "Bot",
)


def text_files() -> list[Path]:
    allowed = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".html"}
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix.casefold() in allowed
    ]


def validate_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        path = SKILL / relative
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")


def validate_frontmatter(errors: list[str]) -> str | None:
    text = SKILL_FILE.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append("SKILL.md must start with YAML frontmatter")
        return None
    frontmatter = match.group(1)
    name_match = re.search(r"(?m)^name:\s*([^\n]+)$", frontmatter)
    description_match = re.search(r"(?m)^description:\s*([^\n]+)$", frontmatter)
    version_match = re.search(r'(?m)^\s+version:\s*["\']?([^\n"\']+)', frontmatter)
    license_match = re.search(r"(?m)^license:\s*([^\n]+)$", frontmatter)
    if not name_match or name_match.group(1).strip() != "translation-workbench":
        errors.append("SKILL.md name must be translation-workbench")
    if not description_match or not description_match.group(1).strip():
        errors.append("SKILL.md description must be non-empty")
    version = version_match.group(1).strip() if version_match else ""
    if not SEMVER_RE.match(version):
        errors.append("SKILL.md metadata.version must be a semantic version such as 0.1.1")
        version = ""
    if not license_match or license_match.group(1).strip() != "MIT":
        errors.append("SKILL.md license must be MIT")
    return version or None


def validate_version_citations(errors: list[str], version: str) -> None:
    """SKILL.md owns the version; every document repeating it has to agree."""
    for name, pattern in VERSION_CITATIONS:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing required file: {name}")
            continue
        match = pattern.search(path.read_text(encoding="utf-8"))
        if not match:
            errors.append(f"{name} does not state a current version")
        elif match.group(1).strip() != version:
            errors.append(
                f"{name} states version {match.group(1).strip()}, "
                f"but SKILL.md metadata.version is {version}"
            )


def validate_links(errors: list[str]) -> None:
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if relative and not (markdown.parent / relative).resolve().exists():
                errors.append(
                    f"Broken Markdown link in {markdown.relative_to(ROOT)}: {target}"
                )


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate_public_content(errors: list[str]) -> None:
    for path in text_files():
        text = path.read_text(encoding="utf-8")
        label = path.relative_to(ROOT)
        if PRIVATE_PATH_RE.search(text):
            errors.append(f"Possible absolute Windows path in {label}")
        if EMAIL_RE.search(text):
            errors.append(f"Email address found in {label}")
        if TOKEN_RE.search(text):
            errors.append(f"Possible access token found in {label}")
        if UNFINISHED_RE.search(text):
            errors.append(f"Unfinished placeholder found in {label}")
        if SKILL in path.parents:
            for term in LEGACY_TERMS:
                if term.casefold() in text.casefold():
                    errors.append(f"Legacy project term {term!r} found in {label}")


def run_tests(errors: list[str]) -> None:
    scripts = SKILL / "scripts"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(scripts),
            "-p",
            "test_*.py",
        ],
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        errors.append("Unit tests failed")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    version = validate_frontmatter(errors) if SKILL_FILE.is_file() else None
    if version:
        validate_version_citations(errors, version)
    validate_links(errors)
    validate_json(errors)
    validate_public_content(errors)
    run_tests(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
