# Add an app

This guide shows you how to add a Django app for a new domain, following the project's conventions. Name apps with a lowercase plural noun. The examples create an app named `orders`.

If you use Claude Code, run the generated project's `/new-app orders` skill instead. It does these steps for you.

1. Create the app package with these files:

   ```text
   website/apps/orders/
   ├── __init__.py
   ├── apps.py
   ├── models.py
   ├── services.py
   ├── exceptions.py
   ├── admin.py
   └── tests/
       └── __init__.py
   ```

2. In `apps.py`, set `name` to the full dotted path:

   ```python
   from django.apps import AppConfig


   class OrdersConfig(AppConfig):
       default_auto_field = "django.db.models.BigAutoField"
       name = "apps.orders"
   ```

3. In `exceptions.py`, add the app's base error:

   ```python
   from apps.core.exceptions import ApplicationError


   class OrdersError(ApplicationError):
       pass
   ```

4. Add `"apps.orders.apps.OrdersConfig"` to `INSTALLED_APPS` in `website/website/settings/components/base.py`.
5. Write your models, then create the first migration:

   ```bash
   make makemigrations ARGS=orders
   ```

6. If the app has an API, create `apps/orders/api/urls.py` with `app_name = "orders"`, and include it in `website/website/api.py`:

   ```python
   path("", include("apps.orders.api.urls")),
   ```

7. Check that nothing is missing:

   ```bash
   make migrate-check
   make test
   ```

To see where models, services, errors and API code go, read {doc}`../explanation/code-layers`. The `polls` app is a complete example.
