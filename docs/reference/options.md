# Template options

Cookiecutter asks for these options when you generate a project.

| Option | Default | Description |
|---|---|---|
| `project_name` | `My Django Project` | Human-readable project name. Used in page titles, the API title and the Wagtail site name. |
| `project_slug` | Derived from `project_name` | Directory name and Docker Compose project name. Lowercase, with spaces and dots replaced by `-`. |
| `description` | `A Django project` | Short description. Used as the OpenAPI description. |
| `author_name` | `Your Name` | Author name. |
| `use_drf` | `y` | Adds Django REST Framework, drf-spectacular and the example `polls` API. |
| `use_wagtail` | `n` | Adds Wagtail CMS and the `cms` app with a home page. |
| `use_vue` | `n` | Adds a Vue 3 single-page app in `frontend/`, served through django-vite. |

## Passing options on the command line

```bash
uvx cookiecutter gh:h0pers/django-combat-template --no-input \
  project_name="Acme Store" use_drf=y use_wagtail=n use_vue=y
```

## Files removed per option

After generation, the template deletes the files for options you turned off.

| Condition | Removed |
|---|---|
| `use_drf=n` | REST framework settings, `apps/core/api/schema.py`, `docstring.py`, `exception_handler.py` and its tests, `apps/polls/api/`, `apps/polls/tests/test_api.py`, the API rule and the `add-endpoint` skill in `.claude/` |
| `use_drf=n` and `use_vue=n` | The whole `apps/polls/` app |
| `use_wagtail=n` | `apps/cms/`, Wagtail settings |
| `use_vue=n` | `frontend/`, Vite settings, the `polls` SPA views, templates and URLs, the frontend rule and the `shadcn-vue` skill in `.claude/`, `.mcp.json` |

## After generation

The template then runs these commands. If one fails, it prints a warning and continues.

| Command | When |
|---|---|
| `npm install --package-lock-only` in `frontend/` | `use_vue=y` |
| `uv lock` | Always |
| `git init`, `git add .`, `git commit -m "Initial commit"` | Always |
