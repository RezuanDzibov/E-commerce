from collections import OrderedDict
from typing import Type

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from rest_framework import exceptions
from rest_framework.serializers import Serializer

from src.cart.models import Item
from src.core.exceptions import exception_raiser
from src.core.serialize_utils import (
    get_serializer_by_data,
    get_serializer_by_objects,
    get_validated_serializer,
    get_serializer_data
)
from src.core.services import BaseService
from src.order.models import Order
from src.order.serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer,
    OrderCreateSerializer
)
from src.order.tasks import send_notify


def order_id_is_valid(order_id: int) -> bool:
    """
    @param order_id: Order model instance id.
    @return: True if valid, if not False.
    @raise: If order_id less than id.
    """
    if order_id < 0:
        raise exception_raiser(exceptions.ValidationError, msg=f"{order_id} less than 0.")
    return True


def get_order(request: HttpRequest, order_id: int) -> Order:
    """
    @param request: Authenticated HttpRequest instance.
    @param order_id: Order model instance id.
    @return: Order model instance.
    @raise: If Order model instance doesn't exist.
    """
    try:
        order = Order.objects.get(customer=request.user, id=order_id)
        return order
    except Order.DoesNotExist:
        exception_raiser(exceptions.NotFound, msg=f"You don't have such an order with the order_id {order_id}.")


def get_orders(request: HttpRequest) -> Type[OrderedDict]:
    """
    Return requesting user orders.
    @param request: Authenticated HttpRequest.
    @return: Serializer data.
    """
    orders = Order.objects.filter(customer=request.user).order_by("-created")
    orders = get_serializer_by_objects(
        serializer_class=OrderSerializer,
        objects=orders,
        many_objects=True
    )
    orders = get_serializer_data(orders)
    return orders


class GetOrder(BaseService):
    """Return order if it exists and has relative to request customer user."""
    def execute(self, order_id: int):
        """
        Performer method.
        @param order_id: Order model instance id.
        @return:
        """
        order_id_is_valid(order_id=order_id)
        order = get_serializer_data(
            get_serializer_by_objects(
                serializer_class=OrderSerializer,
                objects=get_order(request=self.request, order_id=order_id)
            )
        )
        return order


class CreateOrder(BaseService):
    """Create order."""
    def __init__(self, request: HttpRequest):
        super().__init__(request=request)
        self.data = self.request.data.copy()

    def execute(self) -> Type[Serializer]:
        """Performer method."""
        try:
            product_item_id_list_from_request = self._get_product_id_list(self.data.pop("product_item_id_list")[0])
        except KeyError:
            exception_raiser(
                exception_class=exceptions.ValidationError,
                msg="You must provide product_item_id_list like follow [12,43...] or 12,43..."
            )
        product_item_id_list = self._get_valid_id_list(product_item_id_list_from_request)
        order_serializer = get_serializer_data(
            get_validated_serializer(
                get_serializer_by_data(
                    serializer_class=OrderCreateSerializer,
                    data=self.data
                )
            )
        )
        product_items = self._get_product_items(product_item_id_list)
        order = self._create_order(order_serializer=order_serializer)
        self._add_product_item_to_order(order, product_items)
        self._notify_about_created_order(order)
        return get_serializer_by_objects(serializer_class=OrderSerializer, objects=order)

    def _id_list_is_valid(self, invalid_id_list: list) -> bool:
        """
        @param invalid_id_list: list of invalid id.
        @return: True if len of invalid_id_list if 0 or False.
        """
        if len(invalid_id_list) > 0:
            return False
        else:
            return True

    def _validate_product_item_id(self, product_item_id: int, valid_id_list: list, invalid_id_list: list) -> None:
        """
        @param product_item_id: Item model instance id.
        @param valid_id_list: list of valid id.
        @param invalid_id_list: list of invalid id.
        """
        try:
            product_item_id = int(product_item_id)
            if product_item_id > 0:
                valid_id_list.append(product_item_id)
            else:
                invalid_id_list.append(product_item_id)
        except ValueError:
            invalid_id_list.append(product_item_id)

    def _get_valid_id_list(self, id_list_from_request: list) -> list:
        """
        @param id_list_from_request:
        @return: list of valid product item id.
        @raise: If passed any invalid product item id.
        """
        invalid_id_list = []
        valid_id_list = []
        for product_item_id in id_list_from_request:
            self._validate_product_item_id(product_item_id, valid_id_list, invalid_id_list)
        if not self._id_list_is_valid(invalid_id_list):
            exception_raiser(
                exception_class=exceptions.ValidationError,
                msg=f"You have provided invalid data for the ids field.{invalid_id_list}"
            )
        return valid_id_list

    def _get_product_items(self, product_item_id_list: list) -> QuerySet:
        """
        @param product_item_id_list:
        @return: Queryset of Item instance or instances.
        @raise: If don't exist any instances.
        """
        items = Item.objects.filter(id__in=product_item_id_list, cart=self.request.user.cart)
        if items.exists():
            return items
        exception_raiser(exception_class=exceptions.NotFound, msg="You don't have so items in your cart")

    def _create_order(self, order_serializer) -> Order:
        """
        @return: Order model instance.
        """
        order = Order.objects.create(
            customer=self.request.user,
            **order_serializer,
        )
        return order

    def _add_product_item_to_order(self, order: Order, product_items: QuerySet) -> None:
        """
        @param order: Order model instance.
        @param product_items: Queryset of Item instance or instances.
        @return: Queryset of Item instance or instances.
        """
        for item in product_items:
            item.content_object = order
            item.save()

    def _notify_about_created_order(self, order: Order) -> None:
        """
        @param order: Order model instance.
        """
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

    def _get_product_id_list(self, string: str) -> list:
        """
        @param string: product_item_id_list from request.
        @return: List of product_item_id.
        """
        brackets = ["[", "]"]
        for bracket in brackets:
            string = string.replace(bracket, "")
        return list([x.strip() for x in string.split(",")])


class PayOrder(BaseService):
    """Set paid is true."""
    def execute(self, order_id: int) -> Type[OrderedDict]:
        """
        Performer method.
        @param order_id: Order model instance id.
        @return: Serializer data.
        """
        order_id_is_valid(order_id=order_id)
        order = self._get_order(order_id=order_id)
        self._set_paid_is_true(order)
        order = get_serializer_data(get_serializer_by_objects(serializer_class=OrderSerializer, objects=order))
        return order

    def _get_order(self, order_id: int) -> Order:
        """
        Return order if it exists and is paid True.
        @param order_id: Order model instance id.
        @return: Order model instance.
        @raise: If Order model instance paid flag is False.
        """
        order = get_order(self.request, order_id=order_id)
        if order.paid is True:
            exception_raiser(
                exception_class=exceptions.ValidationError,
                msg=f"The order with id {order_id} is paid"
            )
        return order

    def _set_paid_is_true(self, order) -> None:
        """
        @param order: Order model instance.
        """
        order.paid = True
        order.save()


class UpdateOrderStatus(BaseService):
    """Update order delivery status."""
    def execute(self, order_id: int) -> Type[OrderedDict]:
        """
        Performer method.
        @param order_id: Order model  instance id.
        @return: Serializer data.
        """
        delivery_status = self._get_order_serializer().data.get("delivery_status")
        order = self._get_order(order_id)
        self._update_order_status(order, delivery_status)
        order = get_serializer_data(get_serializer_by_objects(serializer_class=OrderSerializer, objects=order))
        return order

    def _get_order_serializer(self) -> Type[Serializer]:
        """
        @return: Validated OrderStatusUpdateSerializer.
        """
        return get_validated_serializer(
            get_serializer_by_data(serializer_class=OrderStatusUpdateSerializer, data=self.request.data)
        )

    def _get_order(self, order_id: int) -> Order:
        """
        @param order_id: Order model instance id.
        @return: Order instance if it exists and paid is True.
        @raise: If Order model instance paid flag is False.
        """
        order = get_order(request=self.request, order_id=order_id)
        if not order.paid:
            exception_raiser(exception_class=exceptions.ValidationError,
                             msg=f"The order with id {order_id} hasn't paid yet")
        return order

    def _update_order_status(self, order: Order, delivery_status: str) -> None:
        """
        @param order: Order model instance.
        @param delivery_status: Order instance delivery status.
        """
        order.delivery_status = delivery_status
        order.save()