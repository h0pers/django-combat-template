import pytest
from django.contrib.auth import get_user_model

from apps.users.models import User


def test_auth_user_model_is_custom_user():
    assert get_user_model() is User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="alice", password="secret")

    assert User.objects.get(pk=user.pk).check_password("secret")
