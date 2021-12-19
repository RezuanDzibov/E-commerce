import random

import pytest
import factory

from pytest_factoryboy import register

from .factories import CategoryFactory, ProductFactory


register(CategoryFactory)
register(ProductFactory)


pytestmark = pytest.mark.django_db


@pytest.fixture
def create_product(category_factory, product_factory):
    category = category_factory.create()
    product = product_factory.create(category=category)
    return product


@pytest.fixture
def create_products(category_factory, product_factory):
    category_factory.reset_sequence(1)
    category_1, category_2 = category_factory.create_batch(2)
    product_factory.create_batch(
        10,
        category=factory.LazyAttribute(lambda obj: random.choice([category_1, category_2]))
    )