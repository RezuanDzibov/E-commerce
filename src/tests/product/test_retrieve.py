import json

import pytest
from django.urls import reverse

from src.product.models import Product
from src.product.serializers import ProductRetrieveSerializer
from src.core.serialize_utils import get_serializer_by_objects
from src.tests.utils import get_dumped_json_serializer


pytestmark = pytest.mark.django_db


def test_product_retrieve_endpoint(api_client, create_product):
    product_serializer = get_serializer_by_objects(
        serializer_class=ProductRetrieveSerializer,
        objects=create_product,
    )
    expected_data = json.loads(get_dumped_json_serializer(product_serializer))
    response = api_client.get(f"{reverse('product:product-detail', args=[product_serializer.data.get('slug')])}")
    assert response.status_code == 200
    assert json.loads(response.content) == expected_data


def test_product_retrieve_endpoint_unmatched_data(api_client, create_products):
    products = Product.objects.all()
    product_serializer = get_serializer_by_objects(
        serializer_class=ProductRetrieveSerializer,
        objects=products,
        many_objects=True
    )
    expected_data = json.loads(get_dumped_json_serializer(product_serializer))
    response = api_client.get(f"{reverse('product:product-detail', args=[product_serializer.data[0].get('slug')])}")
    assert response.status_code == 200
    assert json.loads(response.content) != expected_data


def test_product_retrieve_endpoint_404(api_client):
    response = api_client.get(f"{reverse('product:product-detail', args=['noexistslug'])}")
    assert response.status_code == 404