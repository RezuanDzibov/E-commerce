from rest_framework import permissions, response, status, views, generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from . import services
from . import serializers
from src.item.serializers import ItemSerializer


class CartProducts(views.APIView):
    """ The view that responses products from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'200': ItemSerializer(many=True)})
    def get(self, request):
        items = services.get_cart_products(request)
        return Response(items.data, status=status.HTTP_200_OK)


class ClearAllProductsFromCart(views.APIView):
    """ The view that clears all products from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'204': 'Your cart been cleared.'})
    def delete(self, request):
        services.clear_cart(request=request)
        return Response(data={"detail": "Your cart been cleared."}, status=status.HTTP_204_NO_CONTENT)


class AddProductToCart(generics.GenericAPIView):
    """ The view that adds product to requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CartProductAddSerializer

    @swagger_auto_schema(responses={'201': ItemSerializer(many=True)})
    def post(self, request, *args, **kwargs):
        item = services.AddItemToCart(request=request).execute()
        return response.Response(data=item.data, status=status.HTTP_201_CREATED)


class RemoveProductFromCart(generics.GenericAPIView):
    """ The view that remove product from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CartProductRemoveSerializer

    @swagger_auto_schema(responses={'201': ItemSerializer(many=True), '204': 'The product has just been deleted.'})
    def delete(self, request, *args, **kwargs):
        item = services.RemoveItemFromCart(request=request).execute()
        if item is not None:
            return Response(data=item.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT, data='The product has just been deleted.')
