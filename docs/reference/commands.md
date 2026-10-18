# Make commands

Run these from the root of a generated project. Django runs inside Docker, so commands that need Django use the test image. Run `make help` to print this list.

| Command | Description |
|---|---|
| `make help` | List the available commands. |
| `make up-debug` | Start the development stack with hot reload at <http://localhost>. |
| `make test` | Run the test suite. Builds the `backend:test` image if it doesn't exist. |
| `make test ARGS=<path>` | Run selected tests. Paths are relative to `website/`, for example `ARGS=apps/core/tests/test_django_mode.py`. |
| `make coverage` | Run the test suite with a coverage report. |
| `make test-image` | Rebuild the `backend:test` image. Run it after changing dependencies. |
| `make test-down` | Stop the test database and cache and remove their volumes. |
| `make lint` | Check linting and formatting with Ruff. Needs uv on the host. |
| `make format` | Fix linting and formatting with Ruff. Needs uv on the host. |
| `make makemigrations` | Create migrations for all apps. |
| `make makemigrations ARGS=<app>` | Create migrations for one app. |
| `make migrate-check` | Fail if a model has changes without a migration. |

:::{note}
`make test`, `make coverage`, `make makemigrations` and `make migrate-check` reuse any existing image tagged `backend:test`, even one built from another project. Run `make test-image` when you switch between projects.
:::

## Docker Compose files

| File | Used for |
|---|---|
| `docker-compose.debug.yml` | Local development: Django's development server with the source mounted, PostgreSQL, Redis and Traefik on port 80. |
| `docker-compose.test.yml` | The test runner used by the `make` commands and CI. |
| `docker-compose.yml` | Production. Pulls the images from GHCR. |
| `docker-compose.override.yml` | Optional, per server. Merged automatically and never overwritten by deploys. |
