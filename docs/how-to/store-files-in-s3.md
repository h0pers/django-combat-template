# Store files in S3

This guide shows you how to store uploaded media and static files in S3-compatible storage instead of Docker volumes on the server. It works with AWS S3, Cloudflare R2, Backblaze B2, MinIO and other S3-compatible services. You need it to run the app on more than one server or to serve static files from a CDN.

## Before you begin

You need:

- A project deployed with {doc}`deploy-to-a-vps`
- A bucket and an access key that can read, write and delete objects in it

## Prepare the bucket

The project keeps media under `media/` and static files under `static/` in the same bucket. Media is private and served with signed, expiring URLs. Static files are served with plain URLs, so browsers and CDNs can cache them.

1. Allow public reads of `static/*`. If you use AWS, first turn off **Block public access** for bucket policies on this bucket. Then add a bucket policy like this one, with your bucket name:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::my-project-files/static/*"
       }
     ]
   }
   ```

   If your provider serves public files only through a CDN or custom domain, set that domain up instead, and add it as `DJANGO_AWS_STATIC_CUSTOM_DOMAIN` in the next section.

2. Add a CORS rule that allows `GET` from your domain. Browsers need it to load fonts and JavaScript modules from another origin:

   ```json
   [
     {
       "AllowedOrigins": ["https://example.com"],
       "AllowedMethods": ["GET"],
       "AllowedHeaders": ["*"]
     }
   ]
   ```

## Add the GitHub secrets

1. In your repository, go to **Settings** > **Environments** > **production** and add these secrets:

   | Secret | Value |
   |---|---|
   | `DJANGO_AWS_STORAGE_BUCKET_NAME` | Bucket name, for example `my-project-files` |
   | `DJANGO_AWS_ACCESS_KEY_ID` | Your access key ID |
   | `DJANGO_AWS_SECRET_ACCESS_KEY` | Your secret access key |
   | `DJANGO_AWS_S3_REGION_NAME` | Your region, for example `eu-central-1`. For Cloudflare R2, use `auto`. |

2. If you don't use AWS, also add `DJANGO_AWS_S3_ENDPOINT_URL` with your provider's endpoint, for example `https://<account>.r2.cloudflarestorage.com`.
3. If static files go through a CDN or custom domain, add `DJANGO_AWS_STATIC_CUSTOM_DOMAIN` with that domain, for example `static.example.com`.
4. Deploy by pushing to `master`. During the deploy, `collectstatic` uploads the static files to the bucket.

## Check the result

Run these commands on the server, in the app directory.

1. Find a static file URL in the admin login page, and request it:

   ```bash
   curl -s https://example.com/admin/login/ | grep -o 'https://[^"]*base.css'
   curl -s -o /dev/null -w '%{http_code}\n' <URL from the previous command>
   ```

   The URL points at your bucket or custom domain, and the second command prints `200`.

2. Save a test file and print its URL:

   ```bash
   docker compose exec backend python manage.py shell -c "from django.core.files.base import ContentFile; from django.core.files.storage import default_storage; print(default_storage.url(default_storage.save('check.txt', ContentFile(b'ok'))))"
   ```

   The URL ends with a signature that includes `X-Amz-Signature`. Requesting the full URL returns `200`. Requesting it without the part after `?` returns `403`, which shows that media stays private.

   If the URL without its signature returns `200`, your bucket is public beyond `static/*`. Fix the bucket policy or the CDN setup before you store user files.

3. Delete the test file:

   ```bash
   docker compose exec backend python manage.py shell -c "from django.core.files.storage import default_storage; default_storage.delete('check.txt')"
   ```

Files uploaded before this change stay in the `media-data` volume. They aren't copied to the bucket.
