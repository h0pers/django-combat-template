---
name: new-app
description: Create a new Django app under website/apps/ with this project's standard layout (models, services, exceptions, admin, tests, optional DRF api/v1) and register it. Use when the user asks for a new app, a new domain, or models that don't belong to an existing app.
argument-hint: "<app_name>"
---

# Create a new Django app

App name: `$ARGUMENTS` (lowercase, plural noun, e.g. `orders`). Below, `<app>` is the app name and `<App>` its CamelCase form (`Orders`).

## 1. Check first

- `website/apps/<app>/` must not exist. If the models belong to an existing app, extend that app instead and stop here.
- DRF is enabled when `website/website/settings/components/rest_framework.py` exists. Only then do step 3.

## 2. Create the app package

```
website/apps/<app>/
├── __init__.py              empty
├── apps.py
├── exceptions.py
├── models.py                empty
├── services.py              empty
├── admin.py                 empty
├── migrations/__init__.py   empty
└── tests/__init__.py        empty
```

`apps.py`:

```python
from django.apps import AppConfig


class <App>Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.<app>"
```

`exceptions.py`:

```python
from apps.core.exceptions import ApplicationError


class <App>Error(ApplicationError):
    pass
```

Fill `models.py`, `services.py` and `admin.py` with the `add-service` skill.

## 3. API package (DRF only)

```
website/apps/<app>/api/
├── __init__.py          empty
├── urls.py
└── v1/
    ├── __init__.py      empty
    ├── urls.py
    ├── views.py         empty
    ├── serializers.py   empty
    ├── schema.py        empty
    └── docstring.py     empty
```

`api/urls.py`:

```python
from django.urls import include, path

app_name = "<app>"

urlpatterns = [
    path("v1/", include("apps.<app>.api.v1.urls")),
]
```

`api/v1/urls.py`:

```python
app_name = "v1"

urlpatterns = []
```

Mount it in `website/website/api.py`:

```python
    path("", include("apps.<app>.api.urls")),
```

Add endpoints with the `add-endpoint` skill.

## 4. Register the app

Add `"apps.<app>.apps.<App>Config",` to `INSTALLED_APPS` in `website/website/settings/components/base.py`, after the other entries under `# Custom apps`.

## 5. Finish

1. If models were added: `make makemigrations ARGS=<app>`, then `make migrate-check`.
2. `make format`, `make lint`, `make test`.
3. Tell the user which files were created and what to add next (models and services, then endpoints).
