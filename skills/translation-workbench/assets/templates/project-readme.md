# {{ project_title }}

{{ project_summary }}

## Working languages

| Role | Language |
|---|---|
| Source | {{ source_language }} |
| Target | {{ target_language }} |

## Works and translation units

| Work | Translation-unit structure | Location |
|---|---|---|
| {{ work_title }} | {{ chapter_section_scene_or_other }} | `{{ work_path }}` |

## File map

| Role | Path | Notes |
|---|---|---|
| Source material | `{{ source_path }}` | {{ source_note }} |

Add a row for the working translation when it exists. As each unit progresses, record the actual paths of its source-preparation handoff, drafting notes, preserved initial draft, and finalization notes. The working translation is the file being edited; the initial draft is its unchanged copy from before finalization. Drafting notes record the AI's work, while finalization notes record the user's decisions and stated reasons. Do not list or create files merely to fill this map.

## Project references

Link only the reference documents that currently exist, such as:

- glossary;
- character or speaker profiles;
- background notes;
- translator style;
- source inventory.

## Translation workflow

Source preparation → Translation → User-led finalization

Use the detailed stage instructions supplied by Translation Workbench. Cross-unit distillation uses the separate `translation-distillation` skill only when the user starts it; it is not the next stage after each unit.

## Recommended session usage

Use a separate session for each major stage. At the start, name the project, translation unit, and stage, for example:

```text
Use translation-workbench. Read this README and perform the translation stage for {{ translation_unit }}.
```

This is a recommendation rather than an enforced requirement. Record each stage's work in project files so a later session does not depend on the earlier conversation.

## Project conventions and constraints

Record only durable constraints that affect later translation decisions.
