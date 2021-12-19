import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ["method_name"],
    [
        ("put",),
        ("patch",)
    ]
)
def test_product_update_without_permissions(method_name, api_client):
    api_client_method = getattr(api_client, method_name)
    response = api_client_method(f"{reverse('product:product-list')}")
    assert response.status_code == 401


@pytest.mark.parametrize(
    ["update_data_dict"],
    [
        ({"name": "someanothername"},),
        ({"price": 10000},),
        ({"available": False},),
        ({"small_description": "Some another small description"},)
    ]
)
def test_product_update_patch_method(update_data_dict, staff_api_client, create_product):
    response = staff_api_client.patch(
        f"{reverse('product:product-list')}{create_product.slug}/",
        update_data_dict,
        format="multipart"
    )
    assert response.status_code == 200