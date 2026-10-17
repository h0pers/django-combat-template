"""
Django REST Framework and drf-spectacular settings.
"""

from website.settings import env

# Django Rest Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "PAGE_SIZE": 100,
    "EXCEPTION_HANDLER": "apps.core.api.exception_handler.custom_exception_handler",
}

# drf-spectacular - Swagger Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": env.str("DOCS_TITLE", default="{{ cookiecutter.project_name }} API"),
    "DESCRIPTION": env.str("DOCS_DESCRIPTION", default="{{ cookiecutter.description }}"),
    "VERSION": env.str("DOCS_VERSION", default="1.0.0"),
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]",
}
