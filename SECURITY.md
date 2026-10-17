# Security Policy

## Supported versions

Django Combat is a template, not a released package. Only the latest commit on `master` is supported. Projects generated earlier do not update automatically, so apply fixes to them by hand.

## Reporting a vulnerability

**Please do not report security issues in public issues, discussions or pull requests.**

Report them privately through GitHub instead:

1. Go to the [Security tab](https://github.com/h0pers/django-combat-template/security) of this repository.
2. Click **Report a vulnerability**.
3. Describe the issue, the affected files or settings, and how to reproduce it.

You should get a first reply within 7 days. Once a fix is ready, it is published together with a GitHub security advisory, and you are credited unless you ask not to be.

## Scope

In scope: insecure defaults shipped by the template, for example:

- Django security settings (`website/website/settings/`)
- Traefik, Nginx and Docker configuration (`docker/`, `docker-compose*.yml`, `Dockerfile`)
- the CI and deploy workflows (`.github/workflows/`)
- backup and restore scripts

Out of scope: vulnerabilities in upstream projects (Django, Traefik, PostgreSQL, WAL-G and so on). Report those to the upstream project. If the template pins an affected version, a regular issue or pull request to bump it is fine.
