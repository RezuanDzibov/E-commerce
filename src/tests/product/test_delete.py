import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_product_delete(staff_api_client, create_product):
    response = staff_api_client.delete(
        f"{reverse('product:product-list')}{create_product.slug}/",
    )
    assert response.status_code == 204
