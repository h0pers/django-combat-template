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
docker compose up -d postgres redis
docker compose run --rm backend /docker-release.sh   # migrate, collectstatic, first superuser
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

If the file is absent, defaults apply: `4` workers and a `60`s timeout (see `website/gunicorn.conf.py`). A common starting point is `(2 * CPU cores) + 1`; lower the worker count on servers with little memory.

Each worker keeps its own database connection pool (`DJANGO_DB_POOL_MAX_SIZE`, default `4`). Keep `workers × DJANGO_DB_POOL_MAX_SIZE × servers` below PostgreSQL's `max_connections` (default `100`). Behind PgBouncer in transaction mode, set `DJANGO_DB_POOL=false` and `DISABLE_SERVER_SIDE_CURSORS: True` in the database settings.

## Health Checks

| Endpoint | Checks | Use for |
|---|---|---|
| `/api/health/` | the app responds | Docker healthcheck and zero-downtime deploys |
| `/api/health/ready/` | PostgreSQL and Redis are reachable | load balancers and uptime monitors |

`/api/health/ready/` returns `503` when a dependency is down; the failing check is logged, not returned. Keep it out of the Docker healthcheck: a database outage would mark every container unhealthy, and orchestrators such as Docker Swarm restart unhealthy containers.

## Files in S3

By default media and static files live in Docker volumes on the server and nginx serves them. To run more than one server, or to serve files from a CDN, store them in S3-compatible storage (AWS S3, Cloudflare R2, Backblaze B2, MinIO) by adding these GitHub secrets:

| Secret | Example |
|---|---|
| `DJANGO_AWS_STORAGE_BUCKET_NAME` | `my-project-files` |
| `DJANGO_AWS_ACCESS_KEY_ID` | |
| `DJANGO_AWS_SECRET_ACCESS_KEY` | |
| `DJANGO_AWS_S3_ENDPOINT_URL` | `https://<account>.r2.cloudflarestorage.com` (empty for AWS) |
| `DJANGO_AWS_S3_REGION_NAME` | `auto` or `eu-central-1` |
| `DJANGO_AWS_STATIC_CUSTOM_DOMAIN` | `static.example.com` (optional CDN domain) |

Media goes under `media/` and is served with signed, expiring URLs, so the bucket stays private. Static files go under `static/` with plain URLs so browsers can cache them, which needs two things on the bucket:

- public read access for `static/*`, or a CDN in front of the bucket set as `DJANGO_AWS_STATIC_CUSTOM_DOMAIN`
- a CORS rule allowing `GET` from `https://<your domain>`, needed for fonts and JavaScript modules

The deploy uploads changed static files during `collectstatic`.

## Running on Multiple Servers

The app is stateless; to run it on more than one server:

- Configure [Files in S3](#files-in-s3): local volumes only work on one server.
- Set `GUNICORN_WORKERS` explicitly for each replica and stay within the connection budget above.
- Run `docker-release.sh` once per deploy, never in each replica.
- Keep `postgres` and `postgres-backup` on the same server; they share a volume.
- Point the load balancer at `/api/health/ready/` and keep `/api/health/` as the container healthcheck.

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
