import pytest

from rest_framework.test import APIClient

from product.models import Category


@pytest.fixture
def api_client():
    return APIClient