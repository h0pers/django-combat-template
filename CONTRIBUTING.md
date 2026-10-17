# Contributing to Django Combat

Thanks for helping out. Bug reports, ideas, docs fixes and pull requests are all welcome.

Everyone taking part is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md). If you have a question rather than a change, see [SUPPORT.md](SUPPORT.md). To report a vulnerability, follow [SECURITY.md](SECURITY.md) instead of opening an issue.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-docker/) with Compose v2 (Docker Desktop, Colima or OrbStack all work)
- git
- Node.js 22+ if you touch the Vue option

## How the repository is laid out

| Path | What it is |
|---|---|
| `cookiecutter.json` | Template options and defaults |
| `hooks/post_gen_project.py` | Removes files for options that were not selected |
| `{{cookiecutter.project_slug}}/` | The generated project itself |
| `.github/workflows/template-validation.yml` | CI for the template |

Files listed under `_copy_without_render` in `cookiecutter.json` are copied as-is, without Jinja rendering. These are `.github/**` and `.claude/**` in the generated project, Django templates and the Vue sources. Do not use `{{ cookiecutter.* }}` in those paths. GitHub Actions and Django template syntax would clash with it.

## Making a change

1. Fork the repo and create a branch from `master`, named after [Conventional Commits](https://www.conventionalcommits.org/) types: `feat/...`, `fix/...`, `docs/...`, `ci/...`, `refactor/...`.
2. Make your change.
3. Generate a project and check it works:

   ```bash
   uvx cookiecutter . --no-input -o output/
   # or a specific option combination
   uvx cookiecutter . --no-input -o output/ use_drf=n use_wagtail=y use_vue=y
   ```

4. Inside the generated project, run the same checks CI runs:

   ```bash
   cd output/my-django-project
   uvx pre-commit run --all-files
   make migrate-check
   make test
   ```

   `output/` is git-ignored.

## What CI checks

Every push and pull request generates all 8 combinations of `use_drf`, `use_wagtail` and `use_vue`. For each one, CI:

- runs pre-commit (Ruff lint and format, plus the other hooks)
- builds the Docker `test` image
- fails if models have changes without migrations
- runs the test suite

If your change only affects one option, test that combination locally. CI covers the rest.

## Commits and pull requests

- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/), e.g. `feat: add celery option` or `fix(deploy): wait for healthcheck`.
- Keep a pull request to one logical change.
- Fill in the pull request template, and update the README or `docs/` if behaviour changes.
- A maintainer will review it. Please be patient. This is maintained in spare time.

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
