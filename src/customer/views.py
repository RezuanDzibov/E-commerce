from rest_framework import permissions, response, status, views

from src.cart.services import return_cart_products
from src.order.services import return_orders


class CartItemsAndOrders(views.APIView):
    """ The view responses products and orders related to requested customer """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        orders = return_orders(request=request)
        cart_products = return_cart_products(request=request)
        return response.Response(data={"orders": orders.data, "cart_products": cart_products.data}, status=status.HTTP_200_OK)