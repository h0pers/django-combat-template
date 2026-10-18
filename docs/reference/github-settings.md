# GitHub settings

The deploy workflow reads these from the `production` environment in your repository (**Settings** > **Environments** > **production**).

## Variables

| Variable | Required | Description |
|---|---|---|
| `MY_DOMAIN` | Yes | Domain the site is served on, without `www`, for example `example.com`. |

## Secrets

| Secret | Required | Description |
|---|---|---|
| `VPS_HOST` | Yes | Server host name or IP address. |
| `VPS_USER` | Yes | Deploy user on the server. The app lives in `/home/<VPS_USER>/<repository name>`. |
| `SSH_PRIVATE_KEY` | Yes | Private key for `VPS_USER`. |
| `DJANGO_SECRET_KEY` | Yes | Django secret key. |
| `POSTGRES_USER` | Yes | Database user. |
| `POSTGRES_PASSWORD` | Yes | Database password. |
| `POSTGRES_DB` | Yes | Database name. |
| `PACKAGES_TOKEN` | Yes | Personal access token with the `read:packages` and `delete:packages` scopes. The workflow uses it to delete untagged images from GHCR. |
| `DJANGO_SUPERUSER_USERNAME` | No | Username of the first superuser. |
| `DJANGO_SUPERUSER_PASSWORD` | No | Password of the first superuser. |
| `DJANGO_SUPERUSER_EMAIL` | No | Email address of the first superuser. |
| `DJANGO_AWS_STORAGE_BUCKET_NAME` | No | Turns on S3 storage for media and static files. See {doc}`../how-to/store-files-in-s3`. |
| `DJANGO_AWS_ACCESS_KEY_ID` | With a bucket | Access key ID. |
| `DJANGO_AWS_SECRET_ACCESS_KEY` | With a bucket | Secret access key. |
| `DJANGO_AWS_S3_REGION_NAME` | No | Bucket region. |
| `DJANGO_AWS_S3_ENDPOINT_URL` | No | S3 endpoint for providers other than AWS. |
| `DJANGO_AWS_STATIC_CUSTOM_DOMAIN` | No | CDN or custom domain for static files. |
| `WALG_S3_PREFIX` | No | Turns on S3 backups. See {doc}`../how-to/store-backups-in-s3`. |
| `WALG_LIBSODIUM_KEY` | With S3 | Backup encryption key. The deploy fails if `WALG_S3_PREFIX` is set without it. |
| `WALG_AWS_ACCESS_KEY_ID` | With S3 | Access key ID. |
| `WALG_AWS_SECRET_ACCESS_KEY` | With S3 | Secret access key. |
| `WALG_AWS_REGION` | With S3 | Bucket region. |
| `WALG_AWS_ENDPOINT` | No | S3 endpoint for providers other than AWS. |
| `WALG_AWS_S3_FORCE_PATH_STYLE` | No | `true` for providers that need path-style URLs. |

`GITHUB_TOKEN` is provided by GitHub Actions. The workflows use it to push images to GHCR and to pull them on the server.

## Workflows

| Workflow | Runs on | Does |
|---|---|---|
| `ci.yml` | Pushes to `master`, tags and pull requests. Skips changes that only touch Markdown files. | Builds the images and runs the tests. |
| `deploy.yml` | A successful `CI` run on `master` | Builds and pushes the production images, then deploys them. |
| `pre-commit.yml` | Pushes to `master` and pull requests | Runs the pre-commit hooks. |
