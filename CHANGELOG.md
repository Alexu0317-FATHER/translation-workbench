# Changelog

All notable changes to Translation Workbench are recorded here.

## [Unreleased]

### Changed

- The bundled showcase was replaced by a single screenshot in the README. The
  translated chapters it demonstrated now live in their own repository,
  franz-lohners-chronicle-zh, so this repository stays generic and small.

### Removed

- `showcase/` and the validation that checked its HTML dependencies.

## [0.1.1] - 2026-09-04

### Added

- Simplified Chinese README with bidirectional language links.
- A standalone showcase containing the translated chapter index, five bilingual chapter pages, and their referenced local images.
- Automated validation for local HTML links and image dependencies in the showcase.

### Changed

- Public-content validation now permits project-specific material only inside the explicitly separated showcase while keeping the installable skill generic.

## [0.1.0] - 2026-09-04

### Added

- Cross-runtime Agent Skill for Codex and Claude Code.
- Adaptive project initialization and existing-material intake.
- Source preparation, translation, independent-review, and finalization guidance.
- Templates for project documentation, terminology, context, drafting, and review.
- Read-only context and stage checkers with JSON output.
- Unit and command-line tests for context states, glossary validation, stage gates, review-file protection, and draft checksums.
- MIT License.
