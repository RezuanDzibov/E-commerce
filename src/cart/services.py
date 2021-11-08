from typing import Optional, Union, Type

from django.db.models import F, QuerySet
from rest_framework import exceptions
from rest_framework.serializers import Serializer

from src.cart.serializers import CartProductAddSerializer, CartProductRemoveSerializer
from src.item.models import Item
from src.item.serializers import ItemSerializer
from src.product.models import Product
from src.core.serialize_utils import serialize_objects, serialize_data, validate_serializer
from src.core.exceptions import exception_raiser


def return_cart_products(request) -> Type[Serializer]:
    """ The function for returning items from customer's cart """
    items = request.user.cart.items.all()
    items_serializer = serialize_objects(ItemSerializer, objects=items, many_objects=True)
    return items_serializer


def clear_cart(request):
    """ The function cleaning requested customer's cart """
    request.user.cart.items.all().delete()


class AddItemToCart:
    """ The class adds item to customer cart or update of quantity products in cart """
    def __init__(self, request):
        self.request = request

    def execute(self) -> Type[Serializer]:
        request_data_serializer = validate_serializer(
            serialize_data(serializer_class=CartProductAddSerializer, data=self.request.data)
        )
        product = self.get_product(request_data_serializer)
        item = self.get_item(product)
        if not item.exists():
            item = self.create_item(product, request_data_serializer)
        else:
            item = self.update_item(item, request_data_serializer)
        return serialize_objects(serializer_class=ItemSerializer, objects=item)

    def get_product(self, request_data_serializer) -> Union[Product, exceptions.NotFound]:
        try:
            product = Product.objects.get(slug=request_data_serializer.data.get("product_slug"))
            return product
        except Product.DoesNotExist:
            return exception_raiser(exception_class=exceptions.NotFound, msg="No such product.")

    def get_item(self, product) -> QuerySet:
        item = Item.objects.filter(cart__id=self.request.user.cart.id, product=product)
        return item

    def create_item(self, product, request_data_serializer) -> Item:
        item = Item.objects.create(
            content_object=self.request.user.cart,
            product=product,
            quantity=request_data_serializer.data.get("product_qty")
        )
        return item

    def update_item(self, item, request_data_serializer) -> Item:
        item.update(quantity=F("quantity") + request_data_serializer.data.get("product_qty"))
        return item[0]


class RemoveItemFromCart:
    """ The class removes product to customer cart or update of quantity products in cart """
    def __init__(self, request):
        self.request = request

    def execute(self) -> Optional[ItemSerializer]:
        request_data_serializer = serialize_data(serializer_class=CartProductRemoveSerializer, data=self.request.data)
        product_qty = self.pop_product_qty_from_request_data(request_data_serializer)
        item = self.return_item_from_cart(request_data_serializer)
        if product_qty is not None:
            item = self.reduce_quantity_of_product(item, product_qty)
            return item
        else:
            self.remove_product(item)

    def pop_product_qty_from_request_data(self, request_data_serializer) -> int:
        product_qty = request_data_serializer.data.get("product_qty", None)
        return product_qty

    def return_item_from_cart(self, request_data_serializer) -> Item:
        item = Item.objects.filter(
            cart__id=self.request.user.cart.id,
            product__slug=request_data_serializer.data["product_slug"]
        )
        if item.exists():
            return item
        else:
            raise exception_raiser(exception_class=exceptions.NotFound, msg="No such product.")

    def reduce_quantity_of_product(self, item, product_qty) -> Type[Serializer]:
        item.update(quantity=F("quantity") - product_qty)
        if int(item[0].quantity) == 0:
            item[0].delete()
        return serialize_objects(serializer_class=ItemSerializer, objects=item[0])

    def remove_product(self, item):
        item[0].delete()
