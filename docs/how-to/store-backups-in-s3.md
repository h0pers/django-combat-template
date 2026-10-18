# Store backups in S3

This guide shows you how to send database backups to S3-compatible storage instead of a volume on the server. It works with AWS S3, Cloudflare R2, MinIO and other S3-compatible services.

## Before you begin

You need:

- A project deployed with {doc}`deploy-to-a-vps`
- A bucket and an access key that can read and write it

## Steps

1. Generate an encryption key:

   ```bash
   openssl rand -hex 32
   ```

   Store the key in a password manager. Without it, you can't restore the backups.

2. In your repository, go to **Settings** > **Environments** > **production** and add these secrets:

   | Secret | Value |
   |---|---|
   | `WALG_S3_PREFIX` | Bucket and path, for example `s3://my-bucket/my-project` |
   | `WALG_LIBSODIUM_KEY` | The key from step 1 |
   | `WALG_AWS_ACCESS_KEY_ID` | Your access key ID |
   | `WALG_AWS_SECRET_ACCESS_KEY` | Your secret access key |
   | `WALG_AWS_REGION` | Your region, for example `eu-central-1`. For Cloudflare R2, use `auto`. |

3. If you don't use AWS, also add `WALG_AWS_ENDPOINT` with your provider's endpoint, for example `https://<account>.r2.cloudflarestorage.com`.
4. If you use MinIO or another service that needs path-style URLs, add `WALG_AWS_S3_FORCE_PATH_STYLE` with the value `true`.
5. Deploy by pushing to `master`.

   If you set `WALG_S3_PREFIX` without `WALG_LIBSODIUM_KEY`, the deploy stops with an error and nothing changes on the server.

## Check the result

On the server, in the app directory, take a backup and list the backups:

```bash
docker compose exec postgres-backup backup.sh
docker compose exec postgres-backup wal-g backup-list
```

The list shows a `base_...` backup, and the files appear in your bucket under the prefix you set.

Backups taken before this change stay in the `postgres-backups` volume. They aren't copied to S3.
