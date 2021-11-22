from django.http import HttpRequest
from rest_framework import permissions, response, status, views
from drf_yasg.utils import swagger_auto_schema

from src.customer.serializers import CustomerSerializer
from src.customer.services import get_customer


class CartItemsAndOrders(views.APIView):
    """ The view responses products and orders related to requested customer """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'200': CustomerSerializer()})
    def get(self, request: HttpRequest) -> response.Response:
        customer = get_customer(request=request)
        return response.Response(data=customer.data, status=status.HTTP_200_OK)