# Finalization

Use this stage to merge drafting and review concerns, collect user decisions, apply approved changes, perform a final comparison, and deliver the final translation.

## Inputs

- the project README;
- the source unit;
- the current translation draft;
- drafting notes;
- review notes;
- applicable glossary, character, background, source, and translator-style documents.

Run the finalization preflight:

```text
python <skill-dir>/scripts/check_stage.py finalization --project-root <project-root> --handoff <sourcing-handoff.json> --translation <draft-path> --drafting-notes <drafting-notes-path> --review-notes <review-path>
```

Proceed only after it returns `status: ready`.

## Merge the notes

Compare drafting notes and review notes by source location and issue content.

- Do not duplicate an issue already covered by the review.
- Add drafting-only concerns to the appropriate review section.
- Preserve conflicting interpretations and present them to the user.
- Treat note merging as preparation, not as a user decision.

## Collect user decisions

Process issues in document order unless the user requests another order.

- Use a structured user-input tool only when the options are short and understandable without losing necessary evidence.
- For nuanced translation choices, show the relevant source, current translation, issue, tradeoffs, and recommendation in ordinary conversation.
- Record the user's decision before modifying the translation.
- Do not repeatedly reopen a decision after the user has made it unless new evidence appears.

Mechanical corrections marked during review do not need a separate editorial decision.

## Apply decisions

- Apply user-approved changes and unambiguous mechanical corrections.
- Leave passages unchanged when the user chooses to keep the current translation.
- Preserve document order, formatting, links, images, and annotations unless the user approved a related change.
- Mark each review item completed after its decision has been applied or confirmed as requiring no change.

Allow the user to make their own edits when they want to. Treat the saved file after those edits as the current translation.

## Final check

Read the complete current translation and compare it with the complete source again.

Check completeness, accuracy, order, voice, terminology, notes, formatting, and new mechanical errors introduced during finalization.

- Correct new unambiguous mechanical errors.
- Add any new substantive issue to the review notes and return it to user decision.
- Do not treat earlier review notes as proof that later user edits are correct.

## Durable project knowledge

After the translation is confirmed, identify only decisions that may affect later work. Propose changes to the glossary, character profiles, background notes, source inventory, or translator-style document.

Write those changes only after the user approves them. Do not convert one passage-specific solution into a general project rule.

## Completion

- all review and drafting concerns have recorded outcomes;
- approved changes are reflected in the translation;
- the final source-to-translation comparison is complete;
- durable project-document updates are either approved and written or explicitly declined;
- the user has confirmed the final translation.

Record finalization in the review notes and report the final translation path. The skill ends here. Do not continue into publishing or platform conversion.
