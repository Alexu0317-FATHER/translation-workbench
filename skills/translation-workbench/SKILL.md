---
name: translation-workbench
description: Initialize, organize, start, or continue a source-grounded, multi-stage translation project through source preparation, terminology alignment, drafting, independent review, and user-led finalization. Use when the user explicitly names translation-workbench or asks to start, continue, or organize a structured translation workflow. Do not use for quick one-off translations, publishing, or post-publication formatting.
license: MIT
metadata:
  version: "0.1.0"
---

# Translation Workbench

Guide a translation project from source material to a user-approved final translation. Adapt to the user's languages, material, document structure, and current stage instead of assuming a particular genre, book layout, chapter numbering system, or output channel.

## User interaction

- Follow the user's request. Do not force a setup questionnaire, a fixed opening message, or a particular next stage.
- Inspect the current request and available project files before asking questions. Ask only for missing information that materially changes the work.
- When a decision has a small, clear set of options, prefer a structured user-input tool exposed by the current runtime. Examples include Claude Code's `AskUserQuestion`, Codex's `request_user_input`, or an equivalent tool.
- Use ordinary conversation for paths, document uploads, long explanations, terminology evidence, translation choices, and other open-ended answers.
- If no structured user-input tool is available, ask a concise plain-text question.
- Never treat a tool-selection response as authorization for a different file mutation, external action, or publication.

## Start from the user's situation

1. Read a project-level `README.md` when one exists and appears to describe the translation project.
2. Determine whether the user is creating a new project, adopting existing material, starting a new translation unit, or continuing a named stage.
3. Accept any user-specified work, section, chapter, scene, or other translation unit. Never assume the user starts with the first unit.
4. Preserve the user's existing directory structure when it is workable. For a new project, use the recommended structure in [project initialization](references/project-initialization.md).
5. Treat user-supplied source files and reference documents as read-only inputs. Create derived working documents from the templates without overwriting the originals.
6. Create glossary, character, background, source, or style documents only when real content exists for them. Do not create empty project files merely because templates are available.
7. After initialization, continue only as far as the user's request requires.

For initialization, adoption of existing material, or recovery from an incomplete setup, read [project-initialization.md](references/project-initialization.md).

## Route the requested stage

- **Explain or plan:** Explain the relevant part of the workflow without creating files unless the user asks.
- **Prepare source material:** Read [sourcing.md](references/sourcing.md).
- **Draft a translation:** Read [translation.md](references/translation.md).
- **Independently review a draft:** Read [independent-review.md](references/independent-review.md).
- **Merge decisions and finalize:** Read [finalization.md](references/finalization.md).

If a requested stage lacks its required inputs, report the missing input and stop that stage. Do not silently reconstruct an earlier stage from guesses.

## Session boundaries

- Recommend a separate session for each major stage because it limits context carryover and makes the independent review cleaner.
- Do not require, enforce, or claim to validate how the user organizes sessions.
- Do not promise that a complete project will behave consistently when run in one long session or across untested models.
- At the end of a completed stage, state what was produced and give a short suggested prompt for starting the next stage in a new session.
- A new session must rely on the project README and saved stage artifacts, not on access to the previous conversation.

## Deterministic checks

Use the bundled read-only checkers instead of relying on a model assertion when their inputs are available:

- `scripts/check_translation_context.py` validates a unit's JSON handoff, checks durable terminology against the glossary, verifies selected Markdown sections, and returns the exact context to read.
- `scripts/check_stage.py` checks stage prerequisites, protects an existing review file, and verifies that an independently reviewed draft kept the same SHA-256.

Resolve `<skill-dir>` from this skill's installed location. Resolve project files from the explicit project root or paths recorded in the project README.

```text
python <skill-dir>/scripts/check_translation_context.py --project-root <project-root> --handoff <handoff.json>
python <skill-dir>/scripts/check_stage.py <stage> --project-root <project-root> [stage-specific paths]
```

Treat `status: ready` with an empty `warnings` array as a passed context gate. `material_incomplete`, `terms_pending`, or `blocked` means stop the requested stage and report what remains. `error` means the input or checker invocation must be corrected.

## Invariants

- Keep source meaning, order, scope, and uncertainty intact. Do not add background information to the translation merely because it appears in reference material.
- Search existing project terminology before proposing a new durable term.
- Add or change durable glossary, character, background, or translator-style guidance only after the user has approved the underlying judgment.
- Keep chapter- or passage-specific choices in drafting or review notes instead of turning them into universal project rules.
- During independent review, write only review notes. Do not modify the draft, glossary, or project references.
- During finalization, apply non-mechanical changes only after recording the user's decision.
- Never overwrite an existing review file or a user-supplied source file without explicit authorization.
- Do not generate publication packages, platform-specific formatting, dashboards, or analytics.
- Do not require or spawn subagents. The user may organize sessions however they choose.
- Do not claim that behavior or translation quality has been validated for an untested model or language pair.

## Templates

Templates are under `assets/templates/`. Adapt their language and headings to the user's working language while preserving their information roles.

- `project-readme.md`: project entry point and file map
- `glossary.md`: durable, user-approved terminology
- `character-profiles.md`: character and voice guidance
- `background-notes.md`: background facts and provenance
- `translator-style.md`: durable translation style decisions
- `sources.md`: source and research inventory
- `sourcing-handoff.json`: machine-readable source-preparation handoff
- `drafting-notes.md`: passage-level translation choices
- `review-notes.md`: independent-review findings and decisions
