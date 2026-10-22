# Environment variables

The backend reads these variables from the environment or from `.env` in the project root. `.env.example` lists them with values for local development.

In production, the deploy workflow writes `.env` on the server from your {doc}`GitHub settings <github-settings>`.

## Django

| Variable | Default | Description |
|---|---|---|
| `DJANGO_ENV` | `production` | Settings to load: `development`, `production` or `test`. The debug and test Compose files set it for you. |
| `DJANGO_SECRET_KEY` | None | Secret key. Required in production. Development uses a fixed insecure key. |
| `DJANGO_ALLOWED_HOSTS` | None | Comma-separated host names. Required in production. In production, Compose sets it to `MY_DOMAIN`. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Empty | Comma-separated origins. In production, Compose sets it to `https://<MY_DOMAIN>`. |
| `DJANGO_SECURE_SSL_REDIRECT` | `true` | Production only. Redirects HTTP requests to HTTPS. |
| `DJANGO_LANGUAGE_CODE` | `en-us` | Language code. |
| `DJANGO_TIME_ZONE` | `UTC` | Time zone. |
| `DJANGO_STATIC_ROOT` | `/var/www/static` in the image | Directory that `collectstatic` writes to. Not used when files are stored in S3. |
| `DJANGO_MEDIA_ROOT` | `/var/www/media` in the image | Directory for uploaded files. Not used when files are stored in S3. |
| `DJANGO_MEDIA_URL` | `media/` | URL prefix for uploaded files. |

## Database and cache

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_USER` | None | Database user. Required. |
| `POSTGRES_PASSWORD` | None | Database password. Required. |
| `POSTGRES_DB` | None | Database name. Required. |
| `POSTGRES_HOST` | None | Database host. `postgres` in every Compose file. |
| `POSTGRES_PORT` | None | Database port, usually `5432`. |
| `DATABASE_URL` | Unset | If set, replaces all `POSTGRES_*` variables, for example `postgres://user:pass@host:5432/db`. |
| `CACHE_URL` | None | Redis URL, for example `redis://redis:6379/0`. Also stores sessions, backed by the database. |
| `DJANGO_DB_POOL` | `true` | Production only. Gives each Gunicorn worker a pool of database connections. Set to `false` behind PgBouncer in transaction mode. |
| `DJANGO_DB_POOL_MIN_SIZE` | `1` | Connections each worker keeps open. |
| `DJANGO_DB_POOL_MAX_SIZE` | `4` | Most connections each worker opens. Keep `workers × DJANGO_DB_POOL_MAX_SIZE × servers` below PostgreSQL's `max_connections`. |

## File storage

If `DJANGO_AWS_STORAGE_BUCKET_NAME` is set, media and static files go to S3-compatible storage instead of `DJANGO_MEDIA_ROOT` and `DJANGO_STATIC_ROOT`. See {doc}`../how-to/store-files-in-s3`.

| Variable | Default | Description |
|---|---|---|
| `DJANGO_AWS_STORAGE_BUCKET_NAME` | Unset | Bucket name. Turns on S3 storage. |
| `DJANGO_AWS_ACCESS_KEY_ID` | None | Access key ID. Required with a bucket. |
| `DJANGO_AWS_SECRET_ACCESS_KEY` | None | Secret access key. Required with a bucket. |
| `DJANGO_AWS_S3_REGION_NAME` | Unset | Bucket region, for example `eu-central-1`. `auto` for Cloudflare R2. |
| `DJANGO_AWS_S3_ENDPOINT_URL` | Unset | S3 endpoint for providers other than AWS. |
| `DJANGO_AWS_STATIC_CUSTOM_DOMAIN` | Unset | CDN or custom domain for static file URLs, for example `static.example.com`. |

Media goes under `media/` with signed URLs. Static files go under `static/` with unsigned URLs.

## First user

`docker-release.sh` creates a superuser from these variables if the database has no users. It runs on every deploy and on every start of the development stack.

| Variable | Default in `.env.example` | Description |
|---|---|---|
| `DJANGO_SUPERUSER_USERNAME` | `admin` | Username. |
| `DJANGO_SUPERUSER_PASSWORD` | `admin` | Password. |
| `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | Email address. |

## Email

| Variable | Default | Description |
|---|---|---|
| `DJANGO_EMAIL_HOST` | `localhost` | SMTP host. |
| `DJANGO_EMAIL_PORT` | `25` | SMTP port. |
| `DJANGO_EMAIL_HOST_USER` | Empty | SMTP user. |
| `DJANGO_EMAIL_HOST_PASSWORD` | Empty | SMTP password. |
| `DJANGO_EMAIL_USE_TLS` | `false` | Use TLS for SMTP. |
| `DJANGO_SERVER_EMAIL` | `root@localhost` | Sender of error emails. |
| `DJANGO_DEFAULT_FROM_EMAIL` | `webmaster@localhost` | Default sender. |
| `DJANGO_ADMIN_NAME` | Empty | Name of the admin who receives error emails. |
| `DJANGO_ADMIN_EMAIL` | Empty | Address of the admin who receives error emails. |

## Gunicorn

Production only. Set them per server, as described in {doc}`../how-to/tune-gunicorn`.

| Variable | Default | Description |
|---|---|---|
| `GUNICORN_WORKERS` | `(2 × CPU cores) + 1` | Number of worker processes. |
| `GUNICORN_TIMEOUT` | `60` | Request timeout in seconds. |
| `GUNICORN_LOG_LEVEL` | `info` | Log level. |
| `GUNICORN_PORT` | `8000` | Port Gunicorn listens on inside the container. |

Other Gunicorn settings live in `website/gunicorn.conf.py`. Workers restart after about 1,000 requests to limit memory leaks.

## API docs

Only with `use_drf=y`.

| Variable | Default | Description |
|---|---|---|
| `DOCS_TITLE` | `<project_name> API` | OpenAPI title. |
| `DOCS_DESCRIPTION` | `<description>` | OpenAPI description. |
| `DOCS_VERSION` | `1.0.0` | OpenAPI version. |

## Wagtail

Only with `use_wagtail=y`.

| Variable | Default | Description |
|---|---|---|
| `WAGTAIL_SITE_NAME` | `<project_name>` | Site name shown in the Wagtail admin. |
| `WAGTAILADMIN_BASE_URL` | `http://localhost` | Base URL used in links in Wagtail notification emails and previews. In production, Compose sets it to `https://<MY_DOMAIN>`. |

## Backups

The PostgreSQL containers read these from `walg.env`. The deploy workflow writes `walg.env` from the `WALG_*` GitHub secrets. If the file is empty, backups go to the `postgres-backups` volume.

| Variable | Description |
|---|---|
| `WALG_S3_PREFIX` | Bucket and path, for example `s3://my-bucket/my-project`. |
| `AWS_ENDPOINT` | S3 endpoint. Empty for AWS. |
| `AWS_REGION` | Bucket region. |
| `AWS_ACCESS_KEY_ID` | Access key ID. |
| `AWS_SECRET_ACCESS_KEY` | Secret access key. |
| `AWS_S3_FORCE_PATH_STYLE` | `true` for services that need path-style URLs, such as MinIO. |
| `WALG_LIBSODIUM_KEY` | Encryption key, 32 bytes in hex. Required with S3. |
| `WALG_LIBSODIUM_KEY_TRANSFORM` | Always `hex`. |
