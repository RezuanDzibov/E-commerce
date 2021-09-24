from . import services
from rest_framework import response, status, views, permissions


class AddToOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = services.AddToOrder(request).main()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class PayOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated)

    def post(self, request, *args, **kwargs):
        order = services.pay(request)
        if order is not None:
            return response.Response(data=order.data)
        else:
            return response.Response(data="Order does not exist.", status=status.HTTP_404_NOT_FOUND)

