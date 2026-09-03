# Project initialization

Use this reference when the user asks to create a translation project, provides unorganized existing material, or asks to continue work without a usable project entry point.

## Principle

Initialization is adaptive project intake, not a fixed dialogue. Inspect the user's request and available files first. Ask only for information that cannot be inferred and that materially changes the project.

## Determine the starting situation

### New project

No project README or established translation structure exists.

Determine, when not already clear:

- project or work name;
- source and target languages;
- intended project directory;
- source-material location or supplied text;
- the requested work, section, chapter, scene, or other translation unit;
- desired final format, defaulting to Markdown only when the user has not specified one;
- existing terminology, character, background, source, or style material.

Use `assets/templates/project-readme.md` to create the project README. Create other project documents only when real content exists.

### Existing material without a workflow

Inspect the supplied files with the tools available in the current runtime. The material may be in Word, Markdown, PDF, a spreadsheet, plain text, or another readable format.

Classify useful content by role:

| Material role | Project document template |
|---|---|
| durable terminology | `glossary.md` |
| character, speaker, or voice guidance | `character-profiles.md` |
| setting, subject, or background facts | `background-notes.md` |
| durable translation preferences | `translator-style.md` |
| primary and research sources | `sources.md` |

Create derived project documents from the templates. Do not modify, move, rename, or split the user's original files.

Ask the user only when:

- two sources give conflicting instructions or translations;
- the destination or project boundary is unclear;
- content could reasonably serve different roles and the choice affects later retrieval;
- writing would overwrite an existing project document;
- the material requires a substantive editorial decision.

### Existing translation project

Read the existing README and inspect only the files needed for the requested work. Preserve a workable directory structure. Add missing documentation or mappings rather than reorganizing the project by default.

The user may begin with any work, translation unit, or stage. Never redirect them to a first chapter merely because the project is newly recognized by the skill.

## Project README

The project README is the human- and agent-readable entry point. It should record:

- project purpose and working languages;
- works and translation-unit organization;
- paths and roles of source, translation, and reference material;
- workflow stages used by the project;
- recommended session usage;
- durable project constraints and known limitations.

Use stable headings and direct file links. Do not duplicate the contents of reference documents in the README.

Do not add a separate machine-readable project manifest unless a concrete deterministic script later requires one.

Each prepared translation unit does use a small `sourcing-handoff.json`, because the bundled context and stage checkers require an unambiguous machine-readable handoff. This per-unit file does not replace the project README or store session history.

## User-input tools

Use a structured user-input tool only when a decision has a small, meaningful option set. In Claude Code, prefer `AskUserQuestion` when available. In Codex, prefer `request_user_input` when available. Use ordinary conversation for paths, document uploads, long descriptions, or nuanced editorial choices.

## Completion

Initialization is complete when the project README accurately identifies the project, languages, material locations, and relevant workflow entry points.

Then follow the user's original request:

- stop after initialization if that is all they requested;
- proceed to the named stage if they requested initialization and translation work together;
- report any missing input that prevents the requested stage.
