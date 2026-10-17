import logging
{%- if cookiecutter.use_drf != "y" %}
from http import HTTPStatus
{%- endif %}

{% if cookiecutter.use_drf == "y" -%}
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.core.api.schema import health_ready_schema, health_schema
from apps.core.services import HealthService
{%- else -%}
from django.http import JsonResponse

from apps.core.services import HealthService
{%- endif %}

logger = logging.getLogger(__name__)

CHECKS = {
    "database": HealthService.check_database,
    "cache": HealthService.check_cache,
}


def is_ready() -> bool:
    for name, check in CHECKS.items():
        try:
            check()
        except Exception:
            logger.exception("Health check failed: %s", name)
            return False
    return True
{% if cookiecutter.use_drf == "y" %}

@health_schema
@api_view(["GET"])
def health(request) -> Response:
    return Response({"status": "ok"})


@health_ready_schema
@api_view(["GET"])
def health_ready(request) -> Response:
    if is_ready():
        return Response({"status": "ok"})
    return Response({"status": "error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
{%- else %}

def health(request) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def health_ready(request) -> JsonResponse:
    if is_ready():
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=HTTPStatus.SERVICE_UNAVAILABLE)
{%- endif %}
