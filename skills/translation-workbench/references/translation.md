# Translation

Use this stage to resolve pending terminology, produce a complete target-language draft, and record passage-level translation choices.

## Preflight

Read:

- the project README;
- the complete source unit;
- the sourcing handoff;
- the existing glossary and translator-style document, when present;
- only the character, speaker, background, or source sections selected in the handoff.

Stop and report the missing input when the source or sourcing handoff is incomplete. Do not silently rerun source preparation inside the translation stage.

Run the stage gate before drafting:

```text
python <skill-dir>/scripts/check_stage.py translation --project-root <project-root> --handoff <sourcing-handoff.json>
```

Proceed only after it returns `status: ready`. When it reports `terms_pending`, resolve the terms below, update the handoff and glossary as decided, and run the gate again.

## Resolve pending terminology

For each unresolved term:

1. locate every relevant occurrence in the source unit;
2. check user-provided reference material first;
3. consult authoritative external sources only when needed and available;
4. explain the meaning or effect that must be preserved;
5. present viable target-language candidates, their tradeoffs, and a recommendation;
6. ask the user to decide.

Use a structured user-input tool when the options are short and self-contained. Use ordinary conversation when the decision needs quotations, evidence, or nuanced explanation.

Write a term to the project glossary only after the user approves a durable project-wide translation. Keep passage-specific wordplay, temporary labels, and one-off solutions in drafting notes instead.

If new unresolved terms emerge during drafting, pause at a sensible boundary, add them to the handoff, and resolve them before finalizing the draft.

## Draft the complete translation

- Translate the complete source unit in source order.
- Preserve meaning, uncertainty, voice, relationships, numbers, quotations, and meaningful structure.
- Use confirmed glossary entries and applicable project guidance.
- Use background material only to understand the source; do not add facts the source does not state.
- Adapt sentence and paragraph structure when the target language needs it, without omission, duplication, or invented content.
- Preserve or deliberately rebuild wordplay, irony, register, and cross-passage effects when literal wording would lose them.
- Follow the user's requested output format and the project's existing conventions.

## Drafting notes

Create drafting notes from `assets/templates/drafting-notes.md`.

Record only choices that may need later review:

- ambiguity or competing readings;
- wordplay, idiom, irony, or register;
- non-literal choices made for voice or target-language effect;
- relationships or forms of address that the target language must make explicit;
- unresolved questions that remain after drafting.

Do not record routine literal translations or decisions already established by the glossary.

## Completion conditions

- the target-language draft contains the complete source unit;
- confirmed terminology and relevant project guidance are applied;
- drafting notes capture substantive choices and unresolved questions;
- no pending term has been silently decided by the model.

After completion, report the draft and drafting-notes paths and recommend starting independent review in a new session.
