from django.db.models.query import QuerySet
from rest_framework import exceptions
from src.cart.models import Item
from src.core.services_mixins import SerializerMixin

from .models import Order
from .serializers import (AddtoOrderSerializer, OrderSerializer,
                          PayOrderSerializer)


def return_orders(request) -> OrderSerializer:
    orders = Order.objects.filter(customer=request.user)
    serializered_orders = OrderSerializer(orders, many=True)
    return serializered_orders


class CreateOrder(SerializerMixin):
    serializer_class = AddtoOrderSerializer

    def __init__(self, request):
        self.request = request
        self.data = request.data.copy()

    def main(self) -> OrderSerializer:
        self.ids = self.filter_ids()
        self.items = self.return_items()
        self.order = self.create_order()
        self.add_item_to_order()
        return OrderSerializer(self.order)

    def filter_ids(self) -> list:
        data_ids = self.data.pop("ids")[0].split(",")
        ids = []
        invalid_ids = []
        for id in data_ids:
            try:
                ids.append(int(id))
            except Exception:
                invalid_ids.append(id)
        if len(invalid_ids) > 0:
            raise exceptions.ValidationError(f"You have provided invalid data for the ids field.{invalid_ids}")
        return ids

    def return_items(self) -> QuerySet:
        items = Item.objects.filter(id__in=self.ids, cart__id=self.request.user.cart.id)
        if items.exists():
            return items
        raise exceptions.NotFound("You don't have so items in your cart")

    def create_order(self) -> Order:
        serializer = self.serialize(self.data)
        order = Order.objects.create(
            customer=self.request.user,
            **serializer.validated_data,
            delivery_status="processed"
        )
        return order

    def add_item_to_order(self) -> QuerySet:
        for item in self.items:
            item.content_object = self.order
            item.save()


class PayOrder(SerializerMixin):
    serializer_class = PayOrderSerializer

    def __init__(self, request):
        self.request = request

    def main(self) -> OrderSerializer:
        self.serializer = self.serialize(self.request.data)
        payed_order = self.pay()
        return payed_order

    def pay(self) -> OrderSerializer:
        try:
            order = Order.objects.get(customer=self.request.user, id=self.serializer.data["id"], payed=False)
            order.payed = True
            order.save()
            serializerd_order = OrderSerializer(order)
            return serializerd_order
        except Order.DoesNotExist:
            raise exceptions.NotFound("You do not have such an order.")
