# Finalization

Use this stage to confirm the complete translation with the user, record each decision, apply the decisions together, and check the saved result against the source. The review record is created here; it is not a prerequisite from another stage.

## Inputs and preflight

Read the project README, complete source, current draft, drafting notes, initial-draft snapshot, and applicable project references. Read the complete source and draft before presenting individual passages. Use the drafting notes as leads, not as proof that an interpretation is correct.

Unless the project has another established location for the initial-draft copy, use `initial-draft.md` beside the translation. Start a new finalization with:

```text
python <skill-dir>/scripts/check_stage.py finalization --project-root <project-root> --handoff <sourcing-handoff.json> --translation <draft-path> --initial-draft <snapshot-path> --drafting-notes <drafting-notes-path> --review-notes <review-path>
```

Proceed only after `status: ready`. An existing review record is never overwritten. To continue a finalization already in progress, use the same command with `--resume`; it requires the review record to exist and does not expect the working translation still to equal its initial snapshot.

## Confirm in source order

Present the source and corresponding draft passage in order, with stable source locations where available. For a passage named in the drafting notes, show its recorded choice, source feature, or awkward spot; for other passages, show the source and draft without inventing an issue. Let the user keep, revise, or question each passage.

Create a finalization record from `assets/templates/review-notes.md` at the project's chosen path, defaulting to `review-notes.md` when none is specified. After the user proposes wording, explain any disagreement or, when you agree, write model analysis within the scope below. Present that analysis to the user and ask them to confirm it before marking the passage confirmed or moving to the next passage. Agreement by the model alone does not finalize a passage; save proposed wording and analysis as pending until the user confirms.

How much analysis to write depends on what changed:

- **Draft kept:** write none. Distillation studies only what the user changed, so there is nothing here for it to use.
- **Draft revised:** state what was wrong with the draft and how the final wording solves it: where a reader would stall, misread, or lose the tone, and what the new wording does about it. Do not write praise of the final wording.
- **User already gave a reason:** add only what they did not say, such as which words carry their reason. If there is nothing to add, write none and ask for no confirmation.
- **Typo, punctuation, or a synonym with no difference in meaning:** note the type of change in one line; no confirmation is needed.

For each confirmed passage, record the final wording or “keep draft”, any model analysis, and the user's confirmation in their own words. Record any reasons the user provides in their own words, separately from your analysis. If their words are verbose, as voice dictation often is, you may condense them: remove fillers, repetitions, false starts, mis-transcriptions, and asides unrelated to the decision, and tighten the phrasing, while keeping their reasoning steps, examples, and judgment words. Label a condensed version as such and show it to the user; once they confirm it, it counts as their own words. When the user gives no reason, do not require an additional explanation from them or present your analysis as their words. After confirmation, label the analysis as model-written and user-confirmed. If the analysis is rewritten, the earlier confirmation no longer applies; ask again. Keep conflicting readings visible until the user decides.

Confirmed durable names and verifiable background facts can be updated in their existing reference files as those decisions are made. Passage-specific choices stay in review notes. Leave character voice, reading premises, and cross-unit style proposals for the separate, user-started distillation.

Do not edit the working translation during the passage-by-passage confirmation. Once all passages have outcomes, apply the recorded final wording together. Preserve source order and the project's existing Markdown structure, links, images, and annotations unless the user has chosen a related change.

## Final check

Give the user room to make their own edits. Then reread the current saved translation and compare it with the complete source. Check completeness, meaning, order, voice, terminology, annotations, and new mechanical errors. Correct unambiguous mechanical errors; return new substantive issues to the user and record their decisions. The current file, including user edits, is the text being checked.

Ask the user to confirm the final translation. Record that confirmation and any project-defined handoff information in the review notes. The initial-draft snapshot stays unchanged for later comparison. This stage ends at the confirmed translation and its notes.
