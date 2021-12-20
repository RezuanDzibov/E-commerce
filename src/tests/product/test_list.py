import json

import pytest
from django.db.models import Q
from django.urls.base import reverse
from faker import Faker

from src.product.models import Product
from src.product.serializers import ProductListSerializer
from src.core.serialize_utils import get_serializer_by_objects
from src.tests.utils import get_dumped_json_serializer


pytestmark = pytest.mark.django_db
fake = Faker()


uri = reverse('product:product-list')
price = fake.random_int(min=100, max=10000)
max_price = fake.random_int(min=100, max=10000)
min_price = fake.random_int(min=100, max=10000)


def test_product_list(api_client, create_products):
    products = Product.objects.all()
    product_serializer = get_serializer_by_objects(
        serializer_class=ProductListSerializer,
        objects=products,
        many_objects=True
    )
    expected_data = json.loads(get_dumped_json_serializer(product_serializer))
    response = api_client.get(uri)
    assert response.status_code == 200
    assert json.loads(response.content).get("results") == expected_data


@pytest.mark.parametrize(
    ["filter_name", "filter_expressions_dict"],
    [
        ("max_price", {
            "queryset_filter_expression": Q(price__lte=price),
            "uri_filter_expression": f"max_price={price}"
        }),
        ("min_price", {
            "queryset_filter_expression": Q(price__gte=price),
            "uri_filter_expression": f"min_price={price}"
        }),
        ("available", {
            "queryset_filter_expression": Q(available=True),
            "uri_filter_expression": "available=true"
        }),
        ("unavailable", {
            "queryset_filter_expression": Q(available=False),
            "uri_filter_expression": "available=false"
        }),
        ("category", {
            "queryset_filter_expression": Q(category__id=1),
            "uri_filter_expression": "category=1"
        }),
        ("max_min_prices_available_category", {
                "queryset_filter_expression": Q(
                    price__lte=max_price,
                    price__gte=min_price,
                    available=True,
                    category__id=1
                ),
                "uri_filter_expression": f"max_price={max_price}&min_price={min_price}&available=true&category=1"
        })
    ]
)
def test_product_list_filter(filter_name, filter_expressions_dict, api_client, create_products):
    products = Product.objects.filter(filter_expressions_dict.get("queryset_filter_expression"))
    product_serializer = get_serializer_by_objects(
        serializer_class=ProductListSerializer,
        objects=products,
        many_objects=True
    )
    expected_data = json.loads(get_dumped_json_serializer(product_serializer))
    response = api_client.get(f"{uri}?{filter_expressions_dict.get('uri_filter_expression')}")
    assert response.status_code == 200
    assert json.loads(response.content).get("results") == expected_data


def test_product_list_search_category(api_client, create_products):
    products = Product.objects.all()
    category_name = products[0].category.name
    products = products.filter(category__name__icontains=category_name)
    product_serializer = get_serializer_by_objects(
        serializer_class=ProductListSerializer,
        objects=products,
        many_objects=True
    )
    expected_data = json.loads(get_dumped_json_serializer(product_serializer))
    response = api_client.get(f"{uri}?search={category_name}")
    assert response.status_code == 200
    assert json.loads(response.content).get("results") == expected_data


@pytest.mark.parametrize(
    ["product", "product_filter_attr"],
    [
        (pytest.lazy_fixture("create_product"), "price"),
        (pytest.lazy_fixture("create_product"), "name")
    ]
)
def test_product_list_search(product, product_filter_attr, api_client):
    product_serializer = get_serializer_by_objects(serializer_class=ProductListSerializer, objects=product)
    expected_data = json.loads(get_dumped_json_serializer(product_serializer))
    response = api_client.get(f"{uri}?search={product_serializer.data.get(product_filter_attr)}")
    assert response.status_code == 200
    assert json.loads(response.content).get("results")[0] == expected_data