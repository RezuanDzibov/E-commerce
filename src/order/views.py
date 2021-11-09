from rest_framework import permissions, response, status, views

from . import services


class CreateOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = services.CreateOrder(request).execute()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class PayOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = services.PayOrder(request).execute()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class OrderStatusUpdate(views.APIView):
    def post(self, request, *args, **kwargs):
        order = services.UpdateOrderStatus(request).execute()
        return response.Response(data=order, status=status.HTTP_201_CREATED)
