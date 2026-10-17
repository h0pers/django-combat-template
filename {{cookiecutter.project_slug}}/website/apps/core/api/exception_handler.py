from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from apps.core.exceptions import ApplicationError


def custom_exception_handler(exc: Exception, context: dict) -> Response | None:
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, ApplicationError):
        return Response(
            {"message": exc.message, "extra": exc.extra},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(exc, exceptions.ValidationError):
        response.data = {
            "message": "Validation error",
            "extra": {"fields": response.data},
        }
    elif isinstance(response.data, dict) and "detail" in response.data:
        response.data = {"message": response.data["detail"], "extra": {}}
    else:
        response.data = {
            "message": exc.default_detail,
            "extra": {"detail": response.data},
        }

    return response
