from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from rest_framework import exceptions
from src.cart.models import Item
from src.core.services_mixins import SerializerMixin, serialize_data, serialize_objects, validate_serializer

from .models import Order
from .serializers import (AddtoOrderSerializer, OrderSerializer,
                          PayOrderSerializer)


def return_orders(request: HttpRequest) -> OrderSerializer:
    orders = Order.objects.filter(customer=request.user)
    serialized_orders = serialize_objects(serializer_class=OrderSerializer, objects=orders, many_objects=True)
    return serialized_orders


class CreateOrder(SerializerMixin):

    def __init__(self, request: HttpRequest):
        self.request = request
        self.data = self.request.data.copy()

    def main(self) -> OrderSerializer:
        id_list_from_request = list(self.data.pop("ids")[0].split(","))
        item_ids = self.return_ids(id_list_from_request)
        items = self.return_items(item_ids)
        order = self.create_order()
        self.add_item_to_order(order, items)
        return OrderSerializer(order)

    def return_ids(self, id_list_from_request: list) -> list:
        valid_ids = []
        invalid_ids = []
        for id in id_list_from_request:
            try:
                valid_ids.append(int(id))
            except Exception:
                invalid_ids.append(id)
            finally:
                if len(invalid_ids) > 0:
                    raise exceptions.ValidationError(
                        f"You have provided invalid data for the ids field.{invalid_ids}")
                else:
                    return valid_ids

    def return_items(self, item_ids: list) -> QuerySet:
        items = Item.objects.filter(id__in=item_ids, cart__id=self.request.user.cart.id)
        if items.exists():
            return items
        raise exceptions.NotFound("You don't have so items in your cart")

    def create_order(self) -> Order:
        serializer = validate_serializer(serialize_data(serializer_class=AddtoOrderSerializer, data=self.data, many_objects=True))
        order = Order.objects.create(
            customer=self.request.user,
            **serializer.validated_data,
            delivery_status="processed"
        )
        return order

    def add_item_to_order(self, order: Order, items: QuerySet) -> QuerySet:
        for item in items:
            item.content_object = order
            item.save()


class PayOrder:
    def __init__(self, request):
        self.request = request

    def main(self) -> OrderSerializer:
        serialized_order = serialize_data(serializer_class=PayOrderSerializer, data=self.request.data)
        payed_order = self.pay(serialized_order)
        return payed_order

    def pay(self, serialized_order: PayOrderSerializer) -> OrderSerializer:
        try:
            order = Order.objects.get(customer=self.request.user, id=serialized_order.data["id"], payed=False)
            order.payed = True
            order.save()
            serialized_order = serialize_objects(OrderSerializer, order)
            return serialized_order
        except Order.DoesNotExist:
            raise exceptions.NotFound("You do not have such an order.")
