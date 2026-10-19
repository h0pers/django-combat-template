# AGENTS.md

Instructions for AI coding agents working in this repository. Human docs live in `README.md`. The architecture and the reasons behind these rules are in `docs/architecture.md`: read it before adding models, services or endpoints.

## Stack

- Python 3.14, Django 5.2 LTS, PostgreSQL 17, Redis 8
- `uv` for dependencies (`pyproject.toml` + `uv.lock`), ruff for lint and format, pytest + pytest-django for tests
{%- if cookiecutter.use_drf == "y" %}
- Django REST Framework + drf-spectacular (Swagger UI at `/api/docs/` when `DEBUG` is on)
{%- endif %}
{%- if cookiecutter.use_wagtail == "y" %}
- Wagtail CMS (editor at `/cms/`), pages in `apps/cms`
{%- endif %}
{%- if cookiecutter.use_vue == "y" %}
- Vue 3 + Vite in `frontend/`, rendered through django-vite
- shadcn-vue UI components (`frontend/components.json`); agent skill in `.claude/skills/shadcn-vue`, MCP server in `.mcp.json`
{%- endif %}
- Docker Compose for every environment; production runs behind Traefik and nginx

## Commands

Run from the project root. Django runs inside Docker: don't run `manage.py` or `pytest` on the host.

```bash
make help                 # list all commands
make test                 # full test suite (builds the test image on first run)
make test ARGS=apps/core/tests/test_django_mode.py   # one file; paths are relative to website/
make lint                 # ruff check + format check (needs uv on the host)
make format               # ruff fix + format
make makemigrations       # create migrations (ARGS=<app> for one app)
make migrate-check        # fail on unmigrated model changes
make test-image           # rebuild the test image after changing dependencies
make up-debug             # dev stack with hot reload at http://localhost
```
{%- if cookiecutter.use_vue == "y" %}

Frontend, from `frontend/`: `npm run dev`, `npm run build`, `npm run lint`, `npm run format`.
{%- endif %}

Before you finish a change, run `make format`, `make lint` and `make test`, plus `make migrate-check` if you touched models.

## Layout

```
website/                        Django project root (manage.py lives here)
├── apps/<app>/                 one Django app per domain
│   ├── models.py
│   ├── services.py             <Entity>Service: every database read and write
│   ├── exceptions.py           <App>Error and its subclasses
│   ├── admin.py
{%- if cookiecutter.use_drf == "y" %}
│   ├── api/v1/                 DRF layer: views, serializers, urls, schema, docstring
│   ├── migrations/
│   └── tests/                  test_services.py, test_api.py
├── apps/core/                  cross-app infrastructure: ApplicationError, API exception handler, health check, middleware
{%- else %}
│   ├── views.py
│   ├── migrations/
│   └── tests/                  test_services.py
├── apps/core/                  cross-app infrastructure: ApplicationError, health check, middleware
{%- endif %}
├── apps/users/                 custom User model (AUTH_USER_MODEL = "users.User")
├── utils/                      pure helpers; must not import from apps
├── gunicorn.conf.py            production server config (workers, timeouts)
└── website/
    ├── settings/components/    settings split by topic (base, database, cache, storage, ...)
    ├── settings/environments/  development.py, production.py, test.py
    ├── urls.py
    └── api.py                  mounts each app's api/urls.py under /api/
```

## Conventions

The short version; `docs/architecture.md` has the full explanation.
{%- if cookiecutter.use_drf == "y" or cookiecutter.use_vue == "y" %} `apps/polls/` is the reference implementation: copy its shape.{% endif %}

- **Views never touch the ORM.** Views{% if cookiecutter.use_drf == "y" %} and serializers{% endif %} validate input and shape output. `<Entity>Service` classes in `services.py` do every database read and write.
- **Services** are classes of `@staticmethod` / `@classmethod` methods with keyword-only arguments and type hints. They do database work only: no input validation, no `full_clean()`. Wrap multi-step writes in `@transaction.atomic`. Return querysets with `select_related` / `prefetch_related` already applied.
- **Errors**: `ApplicationError` (`apps/core/exceptions.py`) → `<App>Error` in `apps/<app>/exceptions.py` → `<App><Thing>Error`, e.g. `PollsError` → `PollsClosedError`. Raise them only for rules that depend on database state.{% if cookiecutter.use_drf == "y" %} The API renders them as `400 {"message": ..., "extra": {...}}`.{% endif %}
{%- if cookiecutter.use_drf == "y" %}
- **API (DRF)**:
  - Serializers live in `api/vN/serializers.py`: `ModelSerializer` with an explicit `fields` list, never `"__all__"`.
  - Views are DRF generics, one class per URL: `ListCreateAPIView` for `items/`, `RetrieveUpdateDestroyAPIView` for `items/<id>/`. Class names end in `API`, e.g. `PollListCreateAPI`.
  - Override `get_queryset()` to call the service, and `create()` / `update()` to pass `serializer.validated_data` to the service. Never call `serializer.save()`.
  - Use `@api_view` only for trivial endpoints such as `health`.
  - OpenAPI: `extend_schema(...)` objects in `schema.py`, description text in `docstring.py`, attached with `@extend_schema_view(get=..., post=...)`.
  - Every error has one shape, `{"message": str, "extra": {...}}`; validation errors put field errors under `extra.fields`.
{%- endif %}
- **Users**: use `settings.AUTH_USER_MODEL` or `get_user_model()`, never `django.contrib.auth.models.User`.
- **Style**: ruff (line length 88) decides formatting, so run `make format`. Write multi-item lists (`fields`, `list_display`, ...) one item per line with a trailing comma. Add docstrings only when they explain something non-obvious. No `print` (ruff T20); use `logging`.

## Gotchas

- `DJANGO_ENV` picks the settings (`development`, `production`, `test`) and **defaults to `production`**, which requires `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`. The debug and test compose files set it for you.
- Settings use django-split-settings: all component files share one namespace, so names from `components/base.py` (e.g. `MIDDLEWARE`) are used elsewhere without importing them (ruff `F821` is ignored there). Add a topic as `components/<topic>.py` and register it in `settings/__init__.py`. Read env vars with `from website.settings import env`.
- A new app needs `website/apps/<name>/apps.py` with `name = "apps.<name>"`, an `"apps.<name>.apps.<Name>Config"` entry in `INSTALLED_APPS` (`components/base.py`) and `make makemigrations ARGS=<name>`{% if cookiecutter.use_drf == "y" %}; include its `api/urls.py` in `website/api.py`{% endif %}.
- URL names are namespaced, e.g. `reverse("api:core:health")`{% if cookiecutter.use_drf == "y" %} or `reverse("api:polls:v1:polls")`{% endif %}.
- Tests that hit the database need `@pytest.mark.django_db`.
- One-off deploy steps (migrations, `collectstatic`, bootstrap data) go in `docker-release.sh`, which runs once per deploy. `docker-cmd.sh` only starts the server, because it runs in every replica.
- File storage is local by default and switches to S3 when `DJANGO_AWS_STORAGE_BUCKET_NAME` is set (`components/storage.py`). Use `default_storage` / `FileField`, never paths under `MEDIA_ROOT`.

## Don't

- Edit migrations that are already committed; add a new one instead.
- Hand-edit `.env`{% if cookiecutter.use_vue == "y" %}, `uv.lock` or `frontend/package-lock.json`{% else %} or `uv.lock`{% endif %}. Add Python dependencies with `uv add <pkg>` (`uv add --group dev <pkg>` for tooling), then run `make test-image`.
- Put queries, `.save()` calls or business logic in views, serializers, model `save()` or signals.
- Commit secrets. `.env.example` documents every variable.
