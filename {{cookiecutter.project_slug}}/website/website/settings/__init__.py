"""
Django settings module using django-environ and django-split-settings.

This module loads environment variables and splits settings into logical components.
Environment is selected via DJANGO_ENV variable: development, production, or test.
"""

from pathlib import Path

import environ
from split_settings.tools import include

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize django-environ
env = environ.Env()

# Read .env file if it exists
ENV_FILE = BASE_DIR.parent / ".env"
if ENV_FILE.exists():
    environ.Env.read_env(str(ENV_FILE))

# Determine which environment to use
DJANGO_ENV = env.str("DJANGO_ENV", default="production")

# Component settings (shared across all environments)
components = [
    "components/base.py",
    "components/database.py",
    "components/security.py",
    "components/email.py",
    "components/logging.py",
{%- if cookiecutter.use_drf == "y" %}
    "components/rest_framework.py",
{%- endif %}
    "components/cache.py",
{%- if cookiecutter.use_wagtail == "y" %}
    "components/wagtail.py",
{%- endif %}
{%- if cookiecutter.use_vue == "y" %}
    "components/vite.py",
{%- endif %}
]

# Environment-specific settings
environment = f"environments/{DJANGO_ENV}.py"

# Include all settings
include(*components, environment)
