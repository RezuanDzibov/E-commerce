import pytest
from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


UserModel = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def staff_api_client(api_client, create_user):
    token = Token.objects.get_or_create(user=create_user)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token[0].key)
    return api_client


@pytest.fixture
def create_user():
    user = UserModel.objects.create(
        first_name="some",
        last_name="some",
        email="some_email@gmail.com",
        password="someverystrongpass",
        is_staff=True
    )
    return user