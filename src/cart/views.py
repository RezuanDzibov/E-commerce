from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, response, status, views

from src.item.serializers import ItemSerializer
from . import serializers
from . import services


class CartProductItems(views.APIView):
    """All product items in requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'200': ItemSerializer(many=True)})
    def get(self, request: HttpRequest) -> response.Response:
        items = services.get_cart_product_items(request)
        return response.Response(data={"product items": items}, status=status.HTTP_200_OK)


class ClearAllProductItemsFromCart(views.APIView):
    """Clear all products from requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'204': 'Your cart been cleared.'})
    def delete(self, request: HttpRequest) -> response.Response:
        services.clear_cart(request=request)
        return response.Response(data={"detail": "Your cart been cleared."}, status=status.HTTP_204_NO_CONTENT)


class AddProductToCart(views.APIView):
    """Add product item to requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CartProductItemAddSerializer(),
        responses={'201': ItemSerializer(many=True)}
    )
    def post(self, request: HttpRequest) -> response.Response:
        item = services.AddItemToCart(request=request).execute()
        return response.Response(data=item, status=status.HTTP_201_CREATED)


class ReduceQuantityOfProductItem(views.APIView):
    """Reduce quantity of product item requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CartProductItemReduceSerializer(),
        responses={'201': ItemSerializer(many=True), '204': 'The product has just been deleted.'}
    )
    def delete(self, request: HttpRequest) -> response.Response:
        item = services.ReduceQuantityOfProductItem(request=request).execute()
        if item is not None:
            return response.Response(data=item, status=status.HTTP_201_CREATED)
        return response.Response(status=status.HTTP_204_NO_CONTENT, data='The product has just been deleted.')


class RemoveProductItemFromCart(views.APIView):
    """Remove product from requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=serializers.CartProductItemRemoveSerializer(),
        responses={'204': 'The product has just been deleted.'}
    )
    def delete(self, request: HttpRequest) -> response.Response:
        services.RemoveProductItemFromCart(request=request).execute()
        return response.Response(status=status.HTTP_204_NO_CONTENT, data='The product has just been deleted.')
