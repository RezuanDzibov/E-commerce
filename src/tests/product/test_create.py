import json

import pytest
from django.urls import reverse

from src.product.serializers import ProductRetrieveSerializer
from src.core.serialize_utils import get_serializer_by_objects
from src.tests.utils import get_dumped_json_serializer
from src.tests.product import factories


pytestmark = pytest.mark.django_db


def test_product_create_without_permissions(api_client):
    response = api_client.post(f"{reverse('product:product-list')}")
    assert response.status_code == 401


def test_product_create_endpoint(staff_api_client, create_user):
    category = factories.CategoryFactory.create()
    product = factories.ProductFactory.build(category=category)
    product_serializer = get_serializer_by_objects(
        serializer_class=ProductRetrieveSerializer,
        objects=product,
    )
    expected_data = {k: v for k, v in json.loads(get_dumped_json_serializer(product_serializer)).items() if v}
    expected_data["category"] = category.id
    response = staff_api_client.post(f"{reverse('product:product-list')}", expected_data)
    assert response.status_code == 201
