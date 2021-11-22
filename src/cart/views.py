from django.http import HttpRequest
from rest_framework import permissions, response, status, views
from drf_yasg.utils import swagger_auto_schema

from . import services
from . import serializers
from src.item.serializers import ItemSerializer


class CartProducts(views.APIView):
    """ The view that responses products from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'200': ItemSerializer(many=True)})
    def get(self, request: HttpRequest) -> response.Response:
        items = services.get_cart_products(request)
        return response.Response(items.data, status=status.HTTP_200_OK)


class ClearAllProductsFromCart(views.APIView):
    """ The view that clears all products from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'204': 'Your cart been cleared.'})
    def delete(self, request: HttpRequest) -> response.Response:
        services.clear_cart(request=request)
        return response.Response(data={"detail": "Your cart been cleared."}, status=status.HTTP_204_NO_CONTENT)


class AddProductToCart(views.APIView):
    """ The view that adds product to requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CartProductAddSerializer(),
        responses={'201': ItemSerializer(many=True)}
    )
    def post(self, request: HttpRequest) -> response.Response:
        item = services.AddItemToCart(request=request).execute()
        return response.Response(data=item.data, status=status.HTTP_201_CREATED)


class RemoveProductFromCart(views.APIView):
    """ The view that remove product from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CartProductRemoveSerializer(),
        responses={'201': ItemSerializer(many=True), '204': 'The product has just been deleted.'}
    )
    def delete(self, request: HttpRequest) -> response.Response:
        item = services.RemoveItemFromCart(request=request).execute()
        if item is not None:
            return response.Response(data=item.data, status=status.HTTP_201_CREATED)
        return response.Response(status=status.HTTP_204_NO_CONTENT, data='The product has just been deleted.')
