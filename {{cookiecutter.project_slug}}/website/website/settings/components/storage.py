"""
File storage settings. Media and static files go to S3 when a bucket is configured.
"""

from website.settings import env

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

if env.str("DJANGO_AWS_STORAGE_BUCKET_NAME", default=None):
    S3_OPTIONS = {
        "bucket_name": env.str("DJANGO_AWS_STORAGE_BUCKET_NAME"),
        "access_key": env.str("DJANGO_AWS_ACCESS_KEY_ID"),
        "secret_key": env.str("DJANGO_AWS_SECRET_ACCESS_KEY"),
        "region_name": env.str("DJANGO_AWS_S3_REGION_NAME", default=None),
        "endpoint_url": env.str("DJANGO_AWS_S3_ENDPOINT_URL", default=None),
        "signature_version": "s3v4",
    }

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                **S3_OPTIONS,
                "location": "media",
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                **S3_OPTIONS,
                "location": "static",
                # Unsigned URLs so browsers and CDNs can cache them
                "querystring_auth": False,
                "custom_domain": env.str(
                    "DJANGO_AWS_STATIC_CUSTOM_DOMAIN", default=None
                ),
            },
        },
    }
