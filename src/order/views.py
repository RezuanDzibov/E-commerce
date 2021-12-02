from django.http import HttpRequest
from rest_framework import permissions, response, status, views
from drf_yasg.utils import swagger_auto_schema

from . import services
from . import serializers


class GetOrders(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={"200": serializers.OrderSerializer()}
    )
    def get(self, request: HttpRequest) -> response.Response:
        orders = services.get_orders(request=request)
        return response.Response(data=orders, status=status.HTTP_200_OK)


class GetOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={"200": serializers.OrderSerializer()})
    def get(self, request: HttpRequest, order_id: int):
        order = services.GetOrder(request=request).execute(order_id=order_id)
        return response.Response(data=order, status=status.HTTP_200_OK)


class CreateOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CreateOrderSerializer(),
        responses={"201": serializers.OrderSerializer()},
    )
    def post(self, request: HttpRequest) -> response.Response:
        order = services.CreateOrder(request).execute()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class PayOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={"201": serializers.OrderSerializer()}
    )
    def patch(self, request: HttpRequest, order_id: int) -> response.Response:
        order = services.PayOrder(request).execute(order_id=order_id)
        return response.Response(data=order, status=status.HTTP_201_CREATED)


class UpdateOrderStatus(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={"201": serializers.OrderSerializer()}
    )
    def patch(self, request: HttpRequest, order_id: int) -> response.Response:
        order = services.UpdateOrderStatus(request).execute(order_id=order_id)
        return response.Response(data=order, status=status.HTTP_201_CREATED)
