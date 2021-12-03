from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, response, status, views

from src.item.serializers import ItemSerializer
from .serializers import CartProductItem
from . import services


class ProductItems(views.APIView):
    """All product items in requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'200': ItemSerializer(many=True)})
    def get(self, request: HttpRequest) -> response.Response:
        items = services.get_cart_product_items(request)
        return response.Response(data={"product items": items}, status=status.HTTP_200_OK)


class ClearCart(views.APIView):
    """Clear all products from requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={'204': "Your cart has been cleared."})
    def delete(self, request: HttpRequest) -> response.Response:
        services.clear_cart(request=request)
        return response.Response(data={"detail": "Your cart been cleared."}, status=status.HTTP_204_NO_CONTENT)


class ProductItemAddToCart(views.APIView):
    """Add product item to requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=CartProductItem(),
        responses={'201': ItemSerializer(many=True)}
    )
    def post(self, request: HttpRequest, product_slug: str) -> response.Response:
        item = services.AddItemToCart(request=request).execute(product_slug=product_slug)
        return response.Response(data=item, status=status.HTTP_201_CREATED)


class ProductItemReduceQuantity(views.APIView):
    """Reduce quantity of product item requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=CartProductItem(),
        responses={'201': ItemSerializer(many=True), '204': 'The product has just been deleted.'}
    )
    def patch(self, request: HttpRequest, product_slug: str) -> response.Response:
        item = services.ReduceQuantityOfProductItem(request=request).execute(product_slug)
        if item is not None:
            return response.Response(data=item, status=status.HTTP_201_CREATED)
        return response.Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"detail": f"The product item with slug {product_slug} has just been deleted."}
        )


class ProductItemRemoveFromCart(views.APIView):
    """Remove product from requesting user shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        query_serializer=CartProductItem(),
        responses={'204': "The product item with slug product_slug parameter has just been deleted."}
    )
    def delete(self, request: HttpRequest, product_slug: str) -> response.Response:
        services.RemoveProductItemFromCart(request=request).execute(product_slug=product_slug)
        return response.Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"detail": f"The product item with slug {product_slug} has just been deleted."}
        )
