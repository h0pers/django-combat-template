# Project layout

The files and directories of a generated project with every option turned on.

```text
my-django-project/
├── .claude/                  Claude Code rules, skills and hooks
├── .github/workflows/        ci.yml, deploy.yml, pre-commit.yml
├── .mcp.json                 MCP servers for AI agents: shadcn-vue (use_vue)
├── docker/
│   ├── nginx/                Image that serves /static/ and /media/
│   └── postgres/             PostgreSQL image with WAL-G and the backup scripts
├── docs/architecture.md      Code conventions, adjusted to the options you picked
├── frontend/                 Vue 3 + Vite app (use_vue)
├── website/                  Django project root, where manage.py lives
│   ├── gunicorn.conf.py      Gunicorn settings for production
│   ├── apps/
│   │   ├── core/             ApplicationError, API exception handler, health check, middleware
│   │   ├── users/            Custom User model (AUTH_USER_MODEL = "users.User")
│   │   ├── polls/            Example app (use_drf or use_vue)
│   │   └── cms/              Wagtail pages (use_wagtail)
│   ├── utils/                Helpers that don't import from apps
│   └── website/
│       ├── settings/
│       │   ├── components/   Settings split by topic: base, database, cache, storage, security, ...
│       │   └── environments/ development.py, production.py, test.py
│       ├── api.py            Mounts each app's api/urls.py under /api/
│       └── urls.py
├── AGENTS.md                 Rules for AI coding agents
├── Dockerfile                development, test and production targets
├── docker-cmd.sh             Container start command: Gunicorn, or the development server
├── docker-release.sh         Migrations, collectstatic and first superuser, run once per deploy
├── Makefile
├── docker-compose.yml        Production
├── docker-compose.debug.yml  Local development
├── docker-compose.test.yml   Test runner
├── pyproject.toml            Dependencies and Ruff configuration
└── uv.lock
```

## Inside an app

```text
apps/<app>/
├── models.py
├── services.py       <Entity>Service classes: every database read and write
├── exceptions.py     <App>Error and its subclasses
├── admin.py
├── api/v1/           views.py, serializers.py, urls.py, schema.py, docstring.py (use_drf)
├── migrations/
└── tests/            test_services.py, test_api.py
```

## Dockerfile targets

| Target | Used by | Contains |
|---|---|---|
| `development` | `docker-compose.debug.yml` | Runtime and the `dev` dependency group |
| `test` | `docker-compose.test.yml`, CI | Runtime and the `test` dependency group |
| `production` | `deploy.yml` | Runtime dependencies only, plus the built frontend with `use_vue` |
