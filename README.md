# Django Combat Template

A production-ready [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Django projects, fully containerized with Docker.

## Stack

- **Python 3.11** with [uv](https://github.com/astral-sh/uv) for dependency management
- **Django 5.2** with split settings (`development` / `production` / `test`)
- **PostgreSQL 17** (Alpine)
- **Redis 8.4** for caching
- **Gunicorn** as the WSGI server
- **Traefik** reverse proxy with automatic Let's Encrypt TLS
- **Docker** multi-stage builds (separate `development` and `production` targets)

## Template Options

| Option | Default | Description |
|---|---|---|
| `project_name` | My Django Project | Human-readable project name |
| `project_slug` | auto-generated | Directory and package name (derived from project name) |
| `description` | A Django project | Short project description |
| `author_name` | Your Name | Author name |
| `use_drf` | y | Include Django REST Framework with drf-spectacular OpenAPI docs |

### When `use_drf` is enabled

The template includes DRF, drf-spectacular for OpenAPI schema generation, django-cors-headers, and a pre-configured health check endpoint at `/api/health/`.

## CI/CD

Three GitHub Actions workflows are included:

- **CI** — builds the Docker image and runs the test suite on every push
- **Deploy** — deploys to a VPS via SSH on pushes to `master`
- **Pre-commit** — runs linting checks via pre-commit hooks

## Code Quality

- **Ruff** for linting and formatting
- **pre-commit** hooks for consistent code style
- **pytest** + **coverage** for testing

## Documentation

For setup instructions, local development commands, VPS deployment, and runtime configuration, see the [project README]({{cookiecutter.project_slug}}/README.md) inside the generated project.
