"""
Development environment settings.
"""

import socket

# Debug mode enabled
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Internal IPs for debug toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# Insecure secret key for development only
SECRET_KEY = "django-insecure-0eikswwglid=ukts4l2_b=676m!-q_%154%2z@&l3)n6)cp3#c"

# Disable security features in development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Email backend for development (prints to console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
{%- if cookiecutter.use_vue == "y" %}

DJANGO_VITE["default"]["dev_mode"] = True
{%- endif %}
