from rest_framework import views, permissions
from rest_framework import response
from rest_framework.response import Response
from rest_framework import status
from . import services


class CartItems(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        items = services.return_cart_items(request)
        return Response(items.data, status=status.HTTP_200_OK)


class ClearCart(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        services.clear_cart(request=request)
        return Response(data={"detail": "Your cart benn cleared."})


class AddToCart(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        item = services.add_to_cart(request=request)
        return response.Response(data=item.data, status=status.HTTP_201_CREATED)


class RemoveFromCart(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        item = services.remove_from_cart(request=request)
        if item is not None:
            return Response(data=item.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)
