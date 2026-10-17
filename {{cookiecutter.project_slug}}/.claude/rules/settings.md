---
paths:
  - "website/website/settings/**"
  - ".env.example"
---

# Settings

- Settings use django-split-settings. `website/website/settings/__init__.py` includes every file in `components/` and then `environments/<DJANGO_ENV>.py`; all of them share one namespace.
- Because of the shared namespace, a component can use names defined earlier (e.g. `MIDDLEWARE.append(...)` in `environments/production.py`) without importing them. Ruff `F821` is ignored in these folders for that reason; don't add imports to silence it.
- A new topic (e.g. a third-party package) goes in its own `components/<topic>.py` and must be added to the `components` list in `settings/__init__.py`. Order matters: a file can only use names from files included before it.
- Environment-specific values go in `environments/development.py`, `production.py` or `test.py`, not in components.
- Read environment variables with `from website.settings import env` (`env.str`, `env.bool`, `env.list`, `env.db()`). Give a `default=` unless the value must be set in production.
- Every new environment variable gets an entry in `.env.example`, with a comment if its meaning isn't obvious.
- `DJANGO_ENV` defaults to `production`; the debug and test compose files set it. Never put real secrets in settings files.
