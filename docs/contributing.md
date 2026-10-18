# Contributing

Bug reports, ideas, docs fixes and pull requests are welcome. The full guide is in [CONTRIBUTING.md](https://github.com/h0pers/django-combat-template/blob/master/CONTRIBUTING.md). Questions go through [SUPPORT.md](https://github.com/h0pers/django-combat-template/blob/master/SUPPORT.md), and vulnerabilities through the [security policy](https://github.com/h0pers/django-combat-template/blob/master/SECURITY.md). Everyone taking part follows the [Code of Conduct](https://github.com/h0pers/django-combat-template/blob/master/CODE_OF_CONDUCT.md).

## Change the template

1. Fork the repository and create a branch named after the change type, for example `feat/celery-option` or `fix/deploy-healthcheck`.
2. Make your change.
3. Generate a project and run the checks that CI runs:

   ```bash
   uvx cookiecutter . --no-input -o output/
   cd output/my-django-project
   uvx pre-commit run --all-files
   make migrate-check
   make test
   ```

4. Open a pull request. CI tests all 8 combinations of `use_drf`, `use_wagtail` and `use_vue`.

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/), for example `feat: add celery option`.

## Change these docs

The docs live in `docs/` and are written in [MyST Markdown](https://myst-parser.readthedocs.io/). Read the Docs builds them for every pull request.

1. Build the docs locally:

   ```bash
   uv run --group docs sphinx-build -W --keep-going -b html docs docs/_build/html
   ```

   The build fails on any warning, the same as on Read the Docs.

2. Open `docs/_build/html/index.html` in your browser and check your pages.

### Where a page goes

The docs follow [Diátaxis](https://diataxis.fr/). Decide what the reader is doing, then put the page in the matching section.

| The reader wants to | Section | Title pattern |
|---|---|---|
| Learn by doing, from zero | Tutorial | What they build: "Build and run your first project" |
| Finish a specific task | `how-to/` | The task: "Restore the database" |
| Look up a fact | `reference/` | The thing: "Environment variables" |
| Understand why | `explanation/` | "About …": "About backups" |

Keep the types apart. If a how-to guide starts explaining why, move the explanation to an `explanation/` page and link to it. If a guide lists every option, move the list to `reference/` and link to it.

### Writing rules

Tutorial
: Every step produces a visible result, and the page shows the exact output. Run the tutorial in a fresh project before you change it. Leave out options and alternatives.

How-to guides
: Open with "This guide shows you how to …". Assume the reader knows Django and Docker. Write numbered steps, and put conditions first: "If you use MinIO, add …". End with a way to check that it worked.

Reference
: Describe; don't instruct. Use tables with the same columns for the same kind of thing. Cover every item, and state defaults and limits.

Explanation
: Answer one "why" question. Discuss alternatives and trade-offs. No steps.

### Style

These rules follow the [Google developer documentation style guide](https://developers.google.com/style/highlights).

- Address the reader as "you". Use active voice and present tense: "The deploy runs migrations", not "Migrations will be run".
- Use sentence case for headings.
- Use numbered lists for steps and bulleted lists for everything else.
- Put commands, file names, paths, variables and values in code font. Put UI labels in bold: **Settings** > **Environments**.
- Show the expected output after a command when the reader needs to check it.
- Use descriptive link text, never "click here". Link to other pages with `` {doc}`path` ``.
- Give every image alt text.
- Use unambiguous dates, such as `2026-10-02`, and say when a time is in UTC.
- Document what exists today. Don't announce planned features.
- Keep each fact in one place and link to it, instead of repeating it on several pages.
