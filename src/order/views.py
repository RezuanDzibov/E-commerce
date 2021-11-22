from django.http import HttpRequest
from rest_framework import permissions, response, status, views
from drf_yasg.utils import swagger_auto_schema

from . import services
from . import serializers


class CreateOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CreateOrderSerializer(),
        responses={'201': serializers.OrderSerializer()},
    )
    def post(self, request: HttpRequest) -> response.Response:
        order = services.CreateOrder(request).execute()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class PayOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.PayOrderSerializer(),
        responses={'201': serializers.OrderSerializer()}
    )
    def post(self, request: HttpRequest) -> response.Response:
        order = services.PayOrder(request).execute()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class OrderStatusUpdate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.OrderStatusUpdateSerializer(),
        responses={'201': serializers.OrderSerializer()}
    )
    def post(self, request: HttpRequest) -> response.Response:
        order = services.UpdateOrderStatus(request).execute()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)
