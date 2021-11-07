from typing import Type

from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from rest_framework import exceptions
from rest_framework.serializers import Serializer

from src.cart.models import Item
from src.core.serialize_utils import serialize_data, serialize_objects, validate_serializer
from src.core.exceptions import exception_raiser

from .models import Order
from .serializers import (AddToOrderSerializer, OrderSerializer,
                          PayOrderSerializer)


def return_orders(request: HttpRequest) -> Type[Serializer]:
    orders = Order.objects.filter(customer=request.user)
    orders_serializer = serialize_objects(serializer_class=OrderSerializer, objects=orders, many_objects=True)
    return orders_serializer


class CreateOrder:

    def __init__(self, request: HttpRequest):
        self.invalid_id_list = []
        self.valid_id_list = []
        self.request = request
        self.data = self.request.data.copy()

    def execute(self) -> Type[Serializer]:
        """ Class executor method """
        product_id_list_from_request = list(self.data.pop("product_ids")[0].split(","))
        items_id_list = self.return_valid_id_list(product_id_list_from_request)
        items = self.return_item(items_id_list)
        order = self.create_order()
        self.add_item_to_order(order, items)
        return serialize_objects(serializer_class=OrderSerializer, objects=order)

    def is_id_list_valid(self):
        if len(self.invalid_id_list) > 0:
            return False
        else:
            return True

    def validate_item_id(self, item_id: int):
        try:
            item_id = int(item_id)
            if item_id > 0:
                self.valid_id_list.append(item_id)
            else:
                self.invalid_id_list.append(item_id)
        except ValueError:
            self.invalid_id_list.append(item_id)

    def return_valid_id_list(self, id_list_from_request: list) -> list:
        for item_id in id_list_from_request:
            self.validate_item_id(item_id)
        if self.is_id_list_valid():
            return self.valid_id_list
        else:
            exception_raiser(
                exception_class=exceptions.ValidationError,
                msg=f"You have provided invalid data for the ids field.{self.invalid_id_list}"
            )

    def return_item(self, items_id_list: list) -> QuerySet:
        items = Item.objects.filter(id__in=items_id_list, cart__id=self.request.user.cart.id)
        if items.exists():
            return items
        exception_raiser(exception_class=exceptions.NotFound, msg="You don't have so items in your cart")

    def create_order(self) -> Order:
        order_serializer = validate_serializer(serialize_data(serializer_class=AddToOrderSerializer, data=self.data))
        order = Order.objects.create(
            customer=self.request.user,
            **order_serializer.validated_data,
            delivery_status="processing"
        )
        return order

    def add_item_to_order(self, order: Order, items: QuerySet) -> QuerySet:
        for item in items:
            item.content_object = order
            item.save()


class PayOrder:
    def __init__(self, request):
        self.request = request

    def execute(self) -> Type[Serializer]:
        pay_order_serializer = validate_serializer(serialize_data(serializer_class=PayOrderSerializer, data=self.request.data))
        paid_order = self.set_paid_is_true(pay_order_serializer)
        return paid_order

    def set_paid_is_true(self, pay_order_serializer: Type[Serializer]) -> Type[Serializer]:
        try:
            order = Order.objects.get(customer=self.request.user, id=pay_order_serializer.data.get("id"), paid=False)
            order.paid = True
            order.save()
            order_serializer = serialize_objects(serializer_class=OrderSerializer, objects=order)
            return order_serializer
        except Order.DoesNotExist:
            exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"""You don't have such an order with the id {pay_order_serializer.data.get("id")}."""
            )