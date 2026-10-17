from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.settings import api_settings

from apps.core.api.exception_handler import custom_exception_handler
from apps.core.exceptions import ApplicationError


def test_handler_is_configured():
    assert api_settings.EXCEPTION_HANDLER is custom_exception_handler


def test_application_error():
    response = custom_exception_handler(
        ApplicationError("Poll is closed", extra={"poll_id": 1}), {}
    )

    assert response.status_code == 400
    assert response.data == {"message": "Poll is closed", "extra": {"poll_id": 1}}


def test_django_validation_error():
    response = custom_exception_handler(
        DjangoValidationError({"question": ["This field cannot be blank."]}), {}
    )

    assert response.status_code == 400
    assert response.data == {
        "message": "Validation error",
        "extra": {"fields": {"question": ["This field cannot be blank."]}},
    }


def test_drf_validation_error():
    response = custom_exception_handler(
        exceptions.ValidationError({"choices": ["Required."]}), {}
    )

    assert response.status_code == 400
    assert response.data == {
        "message": "Validation error",
        "extra": {"fields": {"choices": ["Required."]}},
    }


def test_not_found():
    response = custom_exception_handler(Http404(), {})

    assert response.status_code == 404
    assert response.data == {"message": "Not found.", "extra": {}}


def test_structured_detail_is_kept():
    response = custom_exception_handler(
        exceptions.PermissionDenied({"reason": "not_owner"}), {}
    )

    assert response.status_code == 403
    assert response.data == {
        "message": exceptions.PermissionDenied.default_detail,
        "extra": {"detail": {"reason": "not_owner"}},
    }


def test_unhandled_exception_returns_none():
    assert custom_exception_handler(ValueError("boom"), {}) is None
