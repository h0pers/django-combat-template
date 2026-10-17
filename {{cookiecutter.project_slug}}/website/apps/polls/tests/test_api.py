import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.polls.services import PollService


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def url() -> str:
    return reverse("api:polls:v1:polls")


@pytest.mark.django_db
def test_list_polls(client, url):
    PollService.create(question="Favourite colour?", choices=["Red", "Blue"])

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1
    poll = response.data["results"][0]
    assert poll["question"] == "Favourite colour?"
    assert [choice["text"] for choice in poll["choices"]] == ["Red", "Blue"]


@pytest.mark.django_db
def test_create_poll(client, url):
    response = client.post(
        url,
        {"question": "Favourite food?", "choices": ["Pizza", "Sushi"]},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["question"] == "Favourite food?"
    assert [choice["text"] for choice in response.data["choices"]] == ["Pizza", "Sushi"]


@pytest.mark.django_db
def test_create_poll_needs_two_choices(client, url):
    response = client.post(
        url, {"question": "Favourite food?", "choices": ["Pizza"]}, format="json"
    )

    assert response.status_code == 400
    assert response.data["message"] == "Validation error"
    assert "choices" in response.data["extra"]["fields"]
