from typing import Type

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from rest_framework import exceptions
from rest_framework.serializers import Serializer

from src.cart.models import Item
from src.core.serialize_utils import serialize_data, serialize_objects, validate_serializer
from src.core.exceptions import exception_raiser

from .models import Order
from .serializers import (CreateOrderSerializer, OrderSerializer,
                          PayOrderSerializer, OrderStatusUpdateSerializer)
from .tasks import send_notify


def get_orders(request: HttpRequest) -> Type[Serializer]:
    orders = Order.objects.filter(customer=request.user)
    orders_serializer = serialize_objects(serializer_class=OrderSerializer, objects=orders, many_objects=True)
    return orders_serializer


class CreateOrder:
    """ The class creating order  """

    def __init__(self, request: HttpRequest):
        self.request = request
        self.data = self.request.data.copy()

    def execute(self) -> Type[Serializer]:
        """ Class executor method """
        product_item_id_list_from_request = [x.strip() for x in self.data.pop("product_item_id_list")[0].split(",")]
        item_id_list = self.get_valid_id_list(product_item_id_list_from_request)
        items = self.get_product_items(item_id_list)
        order = self.create_order()
        self.add_item_to_order(order, items)
        self.send_notify_about_order(order)
        return serialize_objects(serializer_class=OrderSerializer, objects=order)

    def is_id_list_valid(self, invalid_id_list: list) -> bool:
        if len(invalid_id_list) > 0:
            return False
        else:
            return True

    def validate_product_item_id(self, item_id: int, valid_id_list: list, invalid_id_list: list) -> None:
        try:
            item_id = int(item_id)
            if item_id > 0:
                valid_id_list.append(item_id)
            else:
                invalid_id_list.append(item_id)
        except ValueError:
            invalid_id_list.append(item_id)

    def get_valid_id_list(self, id_list_from_request: list) -> list:
        invalid_id_list = []
        valid_id_list = []
        for item_id in id_list_from_request:
            self.validate_product_item_id(item_id, valid_id_list, invalid_id_list)
        if not self.is_id_list_valid(invalid_id_list):
            exception_raiser(
                exception_class=exceptions.ValidationError,
                msg=f"You have provided invalid data for the ids field.{invalid_id_list}"
            )
        return valid_id_list

    def get_product_items(self, item_id_list: list) -> QuerySet:
        items = Item.objects.filter(id__in=item_id_list, cart=self.request.user.cart)
        if items.exists():
            return items
        exception_raiser(exception_class=exceptions.NotFound, msg="You don't have so items in your cart")

    def create_order(self) -> Order:
        order_serializer = validate_serializer(serialize_data(serializer_class=CreateOrderSerializer, data=self.data))
        order = Order.objects.create(
            customer=self.request.user,
            **order_serializer.validated_data,
        )
        return order

    def add_item_to_order(self, order: Order, items: Item) -> QuerySet:
        for item in items:
            item.content_object = order
            item.save()

    def send_notify_about_order(self, order: Order) -> None:
        product_items = order.items.values("product__name", "product__price", "quantity")
        product_items_info = []
        for product_item in product_items:
            product_items_info.append(
                [{"Product name": product_item["product__name"]},
                 {"Product price": product_item["product__price"]},
                 {"Total price": product_item["product__price"] * product_item["quantity"]},
                 {"Quantity": product_item["quantity"]}],
            )
        send_notify.delay(
            subject=f"{order.customer.first_name} {order.customer.last_name}",
            order_id=order.id,
            order_total_price=order.order_total_price,
            product_items_info=product_items_info,
            receiver_email=order.customer.email
        )


class PayOrder:
    """ The class sets paid is true """

    def __init__(self, request: HttpRequest):
        self.request = request

    def execute(self) -> Type[Serializer]:
        pay_order_serializer = validate_serializer(
            serialize_data(serializer_class=PayOrderSerializer, data=self.request.data))
        paid_order = self.set_paid_is_true(pay_order_serializer)
        return paid_order

    def set_paid_is_true(self, pay_order_serializer: Type[Serializer]) -> Type[Serializer]:
        try:
            order = Order.objects.get(
                customer=self.request.user,
                id=pay_order_serializer.data.get("order_id"),
                paid=False
            )
            order.paid = True
            order.save()
            order_serializer = serialize_objects(serializer_class=OrderSerializer, objects=order)
            return order_serializer
        except Order.DoesNotExist:
            exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"""You don't have such an order with the order_id {pay_order_serializer.data.get("order_id")}."""
            )


class UpdateOrderStatus:
    """ The class updating order's delivery status """

    def __init__(self, request: HttpRequest):
        self.request = request

    def execute(self) -> Type[Serializer]:
        order_id, delivery_status = list(map(self.get_order_serializer().data.get, ("order_id", "delivery_status")))
        order = self.get_order(order_id)
        self.update_order_status(order, delivery_status)
        return serialize_objects(serializer_class=OrderSerializer, objects=order)

    def get_order_serializer(self) -> Type[Serializer]:
        return validate_serializer(
            serialize_data(serializer_class=OrderStatusUpdateSerializer, data=self.request.data)
        )

    def get_order(self, order_id: int) -> Order:
        try:
            order = Order.objects.get(id=order_id)
            if order.paid == False:
                exception_raiser(exception_class=exceptions.ValidationError,
                                 msg=f"The order with id {order_id} hasn't paid")
            return order
        except Order.DoesNotExist:
            exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"""You don't have such an order with the order_id {order_id}."""
            )

    def update_order_status(self, order: Order, delivery_status: str) -> None:
        order.delivery_status = delivery_status
        order.save()
