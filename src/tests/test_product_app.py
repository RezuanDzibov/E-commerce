# import json

import pytest
# import factory

# from model_bakery import baker
# from django.contrib.auth import get_user_model
from django.urls.base import reverse

# from src.product.models import Category, Product

# Customer = get_user_model()


# @pytest.mark.django_db
# def test_category_create():
#     Category.objects.create(name="CPU")
#     assert Category.objects.count() == 1

pytestmark = pytest.mark.django_db


class TestProductEndpoints:

    def test_product_list(self, api_client):
        # factory.django.DjangoModelFactory()

        response = api_client.get(reverse("product-list"))

        assert response.code == 200