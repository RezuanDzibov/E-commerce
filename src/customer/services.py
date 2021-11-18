from src.core.serialize_utils import serialize_objects

from .models import Customer

from . serializers import CustomerSerializer


def get_customer(request):
    customer = Customer.objects.get(email=request.user.email)
    customer_serializer = serialize_objects(serializer_class=CustomerSerializer, objects=customer)
    return customer_serializer