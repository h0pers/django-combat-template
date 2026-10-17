---
paths:
  - "website/apps/**/migrations/**"
---

# Migrations

- Generate migrations with `make makemigrations ARGS=<app>`; don't write schema migrations by hand.
- Never edit or delete a migration that is already committed. Fix mistakes with a new migration.
- A migration you just generated and haven't committed may be deleted and regenerated.
- Data migrations: `RunPython` with a reverse function (`migrations.RunPython.noop` if there's nothing to undo), using `apps.get_model(...)`, never direct model imports.
- Run `make migrate-check` before finishing; it fails when models have changes without a migration.
- Ruff ignores this folder; don't reformat generated migrations.
