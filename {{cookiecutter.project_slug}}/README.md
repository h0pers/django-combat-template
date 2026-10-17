# Django + Docker ❤️

## Local Development

Run `make help` to list all commands.

### Debug (hot reload, mounts source)

```bash
make up-debug
```

Backend available at `http://localhost`.

### Tests

```bash
# Run full test suite (builds the test image on first run)
make test

# Run specific test file
make test ARGS=apps/core/tests/test_django_mode.py

# Run with coverage
make coverage

# Rebuild test image after dependency changes
make test-image

# Stop the test database and cache
make test-down
```

### Lint and migrations

```bash
make lint            # ruff check + format check
make format          # ruff fix + format
make makemigrations  # create migrations (ARGS=<app> to target one app)
make migrate-check   # fail if models have unmigrated changes
```

### Production (local smoke test)

```bash
# Uses pre-built image from GHCR - does not build locally
docker compose up
```

---

## VPS First-Time Setup

Before the first deploy, run these commands on the VPS to register the systemd service. This is a one-time manual step — the deploy workflow does not handle it.

```bash
REPO_NAME="$REPO_NAME"
DEPLOY_USER=$VPS_USER   # the user set in VPS_USER GitHub secret
APP_DIR="/home/$DEPLOY_USER/$REPO_NAME"

sudo tee /etc/systemd/system/$REPO_NAME.service <<SERVICE
[Unit]
Description=$REPO_NAME
After=docker.service network-online.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=300

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable $REPO_NAME.service
```

After this, all subsequent deploys are handled automatically by the GitHub Actions workflow on every push to `master`.

## Per-Server Runtime Configuration

`GUNICORN_WORKERS` and `GUNICORN_TIMEOUT` are not deployed by CI - they are server-specific (depends on CPU/memory). Configure them once by creating `docker-compose.override.yml` on the server. Docker Compose merges it automatically and CI never overwrites it.

```yaml
services:
  backend:
    environment:
      - "GUNICORN_WORKERS=4"
      - "GUNICORN_TIMEOUT=60"
```

Adjust `GUNICORN_WORKERS` to `(2 * CPU cores) + 1`. If the file is absent, defaults (`2` workers, `60`s timeout) apply.

## Database Backups

Backups run automatically with [WAL-G](https://github.com/wal-g/wal-g):

- every change is archived within about a minute (WAL archiving)
- a full base backup is taken nightly at 03:00 UTC (change in `docker/postgres/crontab`), and on first start
- the last 4 full backups are kept

Backups are stored in the `postgres-backups` volume on the server. To store them in S3 instead, add these GitHub secrets:

| Secret | Example |
|---|---|
| `WALG_S3_PREFIX` | `s3://my-bucket/my-project` |
| `WALG_AWS_ENDPOINT` | `https://<account>.r2.cloudflarestorage.com` (empty for AWS) |
| `WALG_AWS_REGION` | `auto` or `eu-central-1` |
| `WALG_AWS_ACCESS_KEY_ID` | |
| `WALG_AWS_SECRET_ACCESS_KEY` | |
| `WALG_LIBSODIUM_KEY` | output of `openssl rand -hex 32` |

The encryption key is required with S3. Keep a copy in a password manager - without it the backups cannot be restored.

Useful commands:

```bash
docker compose exec postgres-backup wal-g backup-list   # list backups
docker compose exec postgres-backup backup.sh           # take a backup now
docker compose logs postgres-backup                     # backup logs
```

### Restore

The restore goes into a new volume, so the current database stays untouched until you switch. `myproject` below is your Compose project name (see `docker volume ls`), times are UTC.

```bash
# 1. Stop the app and database, so no new writes get lost
docker compose stop backend postgres-backup postgres

# 2. Create an empty volume
docker volume create myproject_postgres-data-restored

# 3. Restore into it. Without a time it restores the latest state
docker compose run --rm --no-deps -v myproject_postgres-data-restored:/restore \
  postgres-backup restore.sh "2026-10-02 14:25"
```

Check `restored_up_to` in the output, then switch to the restored volume in `docker-compose.override.yml`:

```yaml
volumes:
  postgres-data:
    name: myproject_postgres-data-restored
    external: true
```

```bash
# 4. Start on the restored database and take a fresh backup
docker compose up -d
docker compose exec postgres-backup backup.sh

# 5. Once everything looks right, remove the old volume
docker volume rm myproject_postgres-data
```
