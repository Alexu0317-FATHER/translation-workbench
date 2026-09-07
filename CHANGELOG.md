# Changelog

All notable changes to Translation Workbench are recorded here.

## [Unreleased]

### Added

- `CONTRIBUTING.md`: how to report a problem, what a workflow change needs to
  argue, and the checks a pull request has to pass.

### Changed

- `scripts/validate_repository.py` no longer hardcodes the version number. It
  reads `metadata.version` out of `SKILL.md`, checks that it is a semantic
  version, and then checks that both READMEs cite the same one. A release bump
  now has a single source, and CI names whichever document was left behind
  instead of only reporting that the number is wrong.
- The bundled showcase was replaced by a single screenshot in the README. The
  translated chapters it demonstrated now live in their own repository,
  franz-lohners-chronicle-zh, so this repository stays generic and small.

### Removed

- `showcase/` and the validation that checked its HTML dependencies.

### Documentation

- The README screenshot was replaced. It used to show a bilingual reading page,
  which separate build scripts produce rather than this skill. In its place is a
  table taken from chapter 4 of the same project: one source line, what the
  independent review flagged, the AI's draft, and the finalized wording. That is
  what the skill actually produces, and it shows why the person has to be in the
  loop.
- Both READMEs were rewritten around what the workflow is for: the AI supplies
  the reasoning behind a rendering, not just the rendering, so that a translator
  whose command of the source language is uneven still keeps every substantive
  decision. Added a worked example from chapter 1, a stage table of what the
  person and the AI each do, an example screenshot, and links to the published
  bilingual chapters.
- Both READMEs now state the installation scope. `npx skills add` installs into
  the current project by default, and `-g` installs into the user account
  instead; neither was mentioned before. The directories a project install
  writes to and the scope flags for `npx skills update` are documented
  alongside them.

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
