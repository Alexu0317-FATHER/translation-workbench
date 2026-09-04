# Contributing

Thanks for taking a look. This is a small project, and issues are more useful to it than pull requests. If English is not comfortable for you, open the issue in Chinese.

## Reporting a problem

Open an [issue](https://github.com/Alexu0317-FATHER/translation-workbench/issues) and include:

- which runtime you were on (Codex, Claude Code, or something else);
- which stage you were in: initialization, source preparation, translation, independent review, or finalization;
- what you asked for and what happened instead;
- the JSON a checker printed, if one was involved.

Please do not paste source text or translations you are not free to share. A short constructed example is easier to act on anyway.

## Suggesting a change to the workflow

Say which stage it belongs to and what problem it solves. The workflow is deliberately stage-by-stage, and every substantive decision is meant to stay with the translator, so a change that removes a decision point needs a reason.

Judgments about a particular translation belong in your own project's notes, not here. This repository is about the workflow.

## If you are opening a pull request

- Run `python scripts/validate_repository.py` from the repository root. It checks the required files, Markdown links, JSON, and public content, and runs the unit tests. It must pass.
- The skill has one canonical copy, at `skills/translation-workbench/`. Do not add a second copy for another runtime.
- `README.md` and `README.zh.md` say the same thing in two languages. If you change one, change both.
- Anything that changes the skill's behavior needs an entry in `CHANGELOG.md` under `[Unreleased]`.
- Keep the installable skill generic. No project-specific names, no absolute paths, no personal material.

## License

Contributions are accepted under the [MIT License](LICENSE), the same terms as the rest of the repository.
