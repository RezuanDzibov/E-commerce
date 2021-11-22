from typing import Type

from django.http import HttpRequest
from rest_framework.serializers import Serializer

from src.core.serialize_utils import serialize_objects

from .models import Customer

from . serializers import CustomerSerializer


def get_customer(request: HttpRequest) -> Type[Serializer]:
    customer = Customer.objects.get(email=request.user.email)
    customer_serializer = serialize_objects(serializer_class=CustomerSerializer, objects=customer)
    return customer_serializer