import json
import pytest

from django.urls.base import reverse
from django.core.serializers.json import DjangoJSONEncoder

from src.product.serializers import ProductCreateUpdateSerializer
from src.core.services_mixins import serialize


pytestmark = pytest.mark.django_db


class TestProductEndpoints:

    def test_product_list(self, api_client, create_products):
        expected_data = json.dumps(serialize(
            ProductCreateUpdateSerializer,
            data=create_products,
            many_objects=True
        ).data, cls=DjangoJSONEncoder)
        response_data = api_client().get(reverse("product:product-list"))
        print(response_data)