# Independent review

Use this stage to review a completed draft against the source and available project evidence while keeping the draft unchanged.

Recommend performing this stage in a new session. Regardless of session choice, work from the saved files listed below rather than relying on the drafting conversation.

## Preflight

Read:

- the project README;
- the complete source unit;
- the completed target-language draft;
- the sourcing handoff;
- the existing glossary and translator-style document, when present;
- only the relevant character, speaker, background, and source sections named in the handoff.

Stop and report when terminology remains pending or a required file is missing.

If a review-notes file already exists, do not overwrite it. Ask whether to continue it, create a new version, or stop.

When file tools are available, record a checksum of the draft before reviewing and verify it again afterward.

Run the preflight gate. Its output includes the draft SHA-256 to retain for the completion check:

```text
python <skill-dir>/scripts/check_stage.py independent-review --project-root <project-root> --handoff <sourcing-handoff.json> --translation <draft-path> --review-notes <planned-review-path>
```

Proceed only after it returns `status: ready` with no failed checks.

## Review sequence

### Read the complete source

Build a whole-unit understanding of meaning, structure, voice, uncertainty, and cross-passage relationships before judging the translation.

### Read the complete translation independently

Read the target text as target-language writing without checking each sentence against the source. Note possible clarity, reference, rhythm, repetition, register, or continuity problems, but do not edit them or assume they are errors.

### Compare source and translation

Check the complete unit in order for:

- omission, duplication, addition, or structural displacement;
- mistranslation, reference, causality, uncertainty, or tone errors;
- names, numbers, quotations, and terminology consistency;
- target-language clarity and coherence;
- character or speaker voice when a profile exists;
- translator-style compliance when a style record exists;
- wordplay, idiom, irony, and cross-passage effects;
- translator notes or annotations already present in the draft.

Only apply character, background, glossary, or style judgments when the corresponding project evidence exists. Do not invent a user's style or treat the reviewer's preference as an error.

## Review notes only

Create review notes from `assets/templates/review-notes.md`.

- Ground every issue in the source text, the target text, or an explicit project rule.
- Record precise source and target locations when the formats permit it.
- Distinguish mechanical corrections from editorial choices.
- Mark spelling, duplicated characters, and unambiguous punctuation errors as direct mechanical corrections.
- Leave wording, meaning, voice, register, segmentation, and localization choices for user decision.
- If no issue is found, still record the scope checked and state that no issue was found.

Do not modify the draft, glossary, character profiles, background notes, or translator-style document during this stage.

After writing review notes, verify that the draft is unchanged:

```text
python <skill-dir>/scripts/check_stage.py review-complete --project-root <project-root> --translation <draft-path> --review-notes <review-path> --expected-draft-sha256 <preflight-sha256>
```

Put the preflight and completion hashes into the two `translation-workbench:draft-sha256-*` comment markers supplied by the review-notes template. Keep those markers unchanged apart from replacing their placeholder values.

## Completion conditions

- source and target texts were each read completely;
- the complete unit was compared in order;
- every recorded issue has explicit evidence;
- every substantive choice is routed to the user;
- the draft is unchanged;
- the review file does not overwrite an earlier review.

After completion, report the review-notes path and recommend starting finalization in a new session.
