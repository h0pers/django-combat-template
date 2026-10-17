from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status

from apps.core.api import docstring

health_schema = extend_schema(
    summary="Check Health",
    description=docstring.HEALTH_DOCS,
    tags=["Health"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=docstring.HEALTH_RESPONSE_DOCS,
        ),
    },
)

health_ready_schema = extend_schema(
    summary="Check Readiness",
    description=docstring.HEALTH_READY_DOCS,
    tags=["Health"],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description=docstring.HEALTH_READY_RESPONSE_DOCS,
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: OpenApiResponse(
            description=docstring.HEALTH_NOT_READY_RESPONSE_DOCS,
        ),
    },
)
