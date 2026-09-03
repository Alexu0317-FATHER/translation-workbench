# Source preparation

Use this stage to obtain and verify source material, identify terminology that may need durable treatment, select relevant project context, and produce a handoff for translation.

## Inputs

- the project README;
- the user's named work and translation unit;
- a source URL, local file, folder, pasted text, or existing project source;
- existing project references, when relevant.

## Obtain the source

Use the tools available in the current runtime.

- **URL:** retrieve the actual source page, preserve its source URL, and verify title, body completeness, order, and visible metadata relevant to the translation.
- **Local file:** read it with an appropriate available document tool. Preserve the original. If the format cannot be read reliably, ask the user for a readable export rather than guessing.
- **Pasted text:** save an unaltered working copy when the user has asked for project-local output.
- **Existing project source:** use the mapped source recorded in the project README.

Normalize a working copy only when later stages need a stable readable form. Record the relationship to the original source. Never silently rewrite the source content while normalizing formatting.

## Identify terminology and context

1. Read the complete source unit before selecting context.
2. Search the existing glossary for names, places, organizations, technical terms, recurring phrases, and other expressions that may require consistency.
3. Record source terms missing from the glossary without inventing a durable translation.
4. Identify only the character, speaker, background, source, and style sections that can change how this unit is understood or translated.
5. Do not load an entire reference collection merely because it exists.

If the project uses character or subject cards, record the exact section identifiers to read. Downstream stages should use the approved handoff instead of repeating context selection from scratch.

## Handoff

Create `sourcing-handoff.json` from `assets/templates/sourcing-handoff.json`. Adapt its location to the existing project structure, but keep the filename or record its path clearly in the project README.

The handoff records:

- source identity and stable path;
- source and target languages;
- verification performed;
- relevant project references;
- glossary terms already covered;
- unresolved source terms;
- material gaps or warnings.

After writing the handoff, run:

```text
python <skill-dir>/scripts/check_translation_context.py --project-root <project-root> --handoff <sourcing-handoff.json>
```

Correct `error` results. Resolve or explicitly record every warning. `material_incomplete` means source preparation is not complete. `terms_pending` is a valid handoff to the translation stage, where the user resolves the listed terms. `ready` means no term decision remains.

## Completion conditions

- the complete source unit is available in a stable readable form;
- its relationship to the original source is recorded;
- relevant existing terminology has been checked;
- unresolved terminology is listed and may be empty;
- relevant context sections are identified;
- missing material or uncertainty is reported instead of hidden.
- the context checker returns `terms_pending` or `ready` without errors.

After completion, report the handoff path and recommend starting the translation stage in a new session.
