# Add a Python dependency

This guide shows you how to add a Python package to a generated project.

1. Add the package with uv:

   - **If the app needs it at runtime:**

     ```bash
     uv add django-filter
     ```

   - **If only development tools need it,** add it to the `dev` group:

     ```bash
     uv add --group dev django-debug-toolbar
     ```

   uv updates `pyproject.toml` and `uv.lock`. Don't edit `uv.lock` by hand.

2. Rebuild the test image, so `make test` uses the new package:

   ```bash
   make test-image
   ```

3. If the debug stack is running, rebuild it:

   ```bash
   docker compose -f docker-compose.debug.yml up --build
   ```

4. Commit `pyproject.toml` and `uv.lock` together.
