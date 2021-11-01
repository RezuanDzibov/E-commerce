import pytest

from rest_framework.test import APIClient
from pytest_factoryboy import register

from .factories import CategoryFactory, ProductFactory


register(CategoryFactory)
register(ProductFactory)


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def create_products(category_factory, product_factory):
    category = category_factory.create()
    products = product_factory.create_batch(3, category=category)
    return products
