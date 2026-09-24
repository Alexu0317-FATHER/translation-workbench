# Translation

Use this stage to resolve pending terminology, produce a complete target-language draft, and record both translation choices and passages that need the user's attention during finalization.

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

- Read the complete source before drafting. Identify important turns and connections across passages before deciding how individual passages work.
- Translate the complete source unit in source order.
- Preserve meaning, uncertainty, voice, relationships, numbers, quotations, and meaningful structure.
- Use confirmed glossary entries and applicable project guidance.
- Use background material only to understand the source; do not add facts the source does not state.
- Adapt sentence and paragraph structure when the target language needs it, without omission, duplication, or invented content.
- Preserve or deliberately rebuild wordplay, irony, register, and cross-passage effects when literal wording would lose them.
- Follow the user's requested output format and the project's existing conventions.

After drafting, read the complete target text again. Check relationships across sentences and paragraphs, not just the wording of each sentence. Where relevant to the target language, pay particular attention to these breaks:

- a subject carried over from the preceding sentence that becomes unclear after a full stop;
- a cause and result separated into sentences whose relationship the reader cannot follow;
- a sentence that repeats the preceding sentence without adding anything.

These are places to inspect in context. A matching surface pattern does not by itself prove the translation needs changing.

## Drafting notes

Create drafting notes from `assets/templates/drafting-notes.md`.

Organize the notes into three parts:

1. **Choices made.** Record ambiguity, wordplay, idiom, irony, voice, non-literal handling, and relationships or forms of address that the target language makes explicit. Describe this passage's actual choice, not a rule for future passages.
2. **Source features to inspect.** List source passages whose syntax, idiom, delayed explanation, or other project-relevant feature may be difficult to carry into the target language. Include their locations and corresponding draft wording. List them without declaring that the translation did or did not succeed; the user will judge during finalization.
3. **Places that still read awkwardly.** Read the entire draft and list each passage the drafter still finds unclear or hard to read, including relevant entries from the second part. Say where a reader may stumble. Do not silently repair or discard a concern merely because the draft is grammatical.

Use stable source locations when the source format permits them. Do not record routine literal translations or decisions already established by the glossary. Record only work actually done; do not invent alternatives merely to reject them.

## Preserve the initial draft

When the draft and all three note sections are complete, save an unchanged copy before finalization. Unless the project already defines a snapshot path, use `initial-draft.md` beside the working translation and record its path in the drafting notes. If that path already exists, inspect it rather than overwriting it. A project may also retain a version-control revision, but the skill's stage check uses the saved copy so it works without Git.

## Completion conditions

- the target-language draft contains the complete source unit;
- confirmed terminology and relevant project guidance are applied;
- drafting notes capture substantive choices and unresolved questions;
- drafting notes contain the source-feature list and remaining awkward passages, even when either list is empty;
- the initial draft can be retrieved without reconstructing it from later edits;
- no pending term has been silently decided by the model.

After completion, report the draft, drafting notes, and initial-draft location; recommend starting user-led finalization in a new session.
