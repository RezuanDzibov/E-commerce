from rest_framework import permissions, response, status, views

from . import services


class CreateOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = services.CreateOrder(request).main()
        return response.Response(data=order.data, status=status.HTTP_201_CREATED)


class PayOrder(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order = services.PayOrder(request).main()
        return response.Response(data=order.data)
