"""
Test environment settings.
"""

# Debug mode enabled for better error messages
DEBUG = True

# Allow all hosts in testing
ALLOWED_HOSTS = ["*"]

# Use a simple secret key for tests
SECRET_KEY = "django-insecure-test-key-not-for-production"

# Disable security features in tests
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Disable logging during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
        "level": "CRITICAL",
    },
}

# Email backend for tests (doesn't send emails)
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
