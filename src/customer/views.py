from rest_framework import permissions, response, status, generics
from drf_yasg.utils import swagger_auto_schema

from src.customer.serializers import CustomerSerializer
from src.customer.services import get_customer


class CartItemsAndOrders(generics.GenericAPIView):
    """ The view responses products and orders related to requested customer """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'200': CustomerSerializer()})
    def get(self, request):
        customer = get_customer(request=request)
        return response.Response(data=customer.data, status=status.HTTP_200_OK)