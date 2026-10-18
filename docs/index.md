# Django Combat

![Django Combat banner: a Django project shipped to a VPS with HTTPS and backups](assets/thumbnail.png)

Django Combat is a [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Django projects that deploy to a single VPS. A generated project includes Docker images, a GitHub Actions pipeline with zero-downtime rollouts, automatic HTTPS through Traefik, and PostgreSQL with continuous backups and point-in-time restore.

These docs are for developers who generate a project from the template and run it in production.

## Find what you need

{doc}`Tutorial <tutorial>`
: New to Django Combat? Start here. You generate a project, run it on your machine, call its API and run its tests.

{doc}`How-to guides <how-to/index>`
: Steps for specific tasks, such as deploying to a VPS, storing backups and files in S3 or restoring the database.

{doc}`Reference <reference/index>`
: Template options, `make` commands, environment variables, GitHub secrets, endpoints and the project layout.

{doc}`Explanation <explanation/index>`
: How the production stack, the deploy pipeline, the code layers and the backups work, why they are built that way, and how the project grows past one server.

```{toctree}
:hidden:
:caption: Tutorial

tutorial
```

```{toctree}
:hidden:
:caption: How-to guides
:maxdepth: 2

how-to/index
```

```{toctree}
:hidden:
:caption: Reference
:maxdepth: 2

reference/index
```

```{toctree}
:hidden:
:caption: Explanation
:maxdepth: 2

explanation/index
```

```{toctree}
:hidden:
:caption: Project

contributing
```
