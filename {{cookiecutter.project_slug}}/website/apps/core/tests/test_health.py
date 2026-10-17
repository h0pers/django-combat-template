from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.urls import reverse


def fail() -> None:
    raise ConnectionError


def test_health(client):
    response = client.get(reverse("api:core:health"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_health_ready(client):
    response = client.get(reverse("api:core:health-ready"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
@pytest.mark.parametrize("check", ["database", "cache"])
def test_health_ready_fails_when_dependency_is_down(client, check):
    with patch.dict("apps.core.api.views.CHECKS", {check: fail}):
        response = client.get(reverse("api:core:health-ready"))

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert response.json() == {"status": "error"}
