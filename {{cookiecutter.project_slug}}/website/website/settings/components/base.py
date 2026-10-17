"""
Base Django settings - shared configuration across all environments.
"""

from website.settings import BASE_DIR, env

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
{%- if cookiecutter.use_wagtail == "y" %}
    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
{%- endif %}
{%- if cookiecutter.use_vue == "y" %}
    "django_vite",
{%- endif %}
{%- if cookiecutter.use_drf == "y" %}
    # Third-party libraries
    "rest_framework",
    "drf_spectacular",
{%- endif %}
    # Custom apps
    "apps.core.apps.CoreConfig",
    "apps.users.apps.UsersConfig",
{%- if cookiecutter.use_wagtail == "y" %}
    "apps.cms.apps.CmsConfig",
{%- endif %}
{%- if cookiecutter.use_drf == "y" or cookiecutter.use_vue == "y" %}
    "apps.polls.apps.PollsConfig",
{%- endif %}
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
{%- if cookiecutter.use_wagtail == "y" %}
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
{%- endif %}
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"

AUTH_USER_MODEL = "users.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = env.str("DJANGO_LANGUAGE_CODE", default="en-us")

TIME_ZONE = env.str("DJANGO_TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=None)

STATICFILES_DIRS = [BASE_DIR / "static"]


# Media files
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default="")

MEDIA_URL = env.str("DJANGO_MEDIA_URL", default="media/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
