from rest_framework import permissions, response, status, views
from rest_framework.response import Response

from . import services


class CartProducts(views.APIView):
    """ The view that responses products from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        items = services.return_cart_items(request)
        return Response(items.data, status=status.HTTP_200_OK)


class ClearAllProductsFromCart(views.APIView):
    """ The view that clears all products from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        services.clear_cart(request=request)
        return Response(data={"detail": "Your cart been cleared."})


class AddProductToCart(views.APIView):
    """ The view that adds product to requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        item = services.AddItemToCart(request=request).main()
        return response.Response(data=item.data, status=status.HTTP_201_CREATED)


class RemoveProductFromCart(views.APIView):
    """ The view that remove product from requested customer's shopping cart """
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        item = services.RemoveItemFromCart(request=request).main()
        if item is not None:
            return Response(data=item.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)
