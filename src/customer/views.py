from rest_framework import permissions, response, status, views
from src.cart.services import return_cart_items
from src.order.services import return_orders


class CartItemsAndOrders(views.APIView):
    """ The view responses products and orders related to requested customer """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        orders = return_orders(request=request)
        cart_items = return_cart_items(request=request)
        return response.Response(data={"orders": orders.data, "cart_items": cart_items.data}, status=status.HTTP_200_OK)