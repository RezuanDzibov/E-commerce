from typing import Optional, Union

from django.db.models import F, QuerySet
from rest_framework import exceptions

from src.cart.serializers import CartProductAddSerializer, CartProductRemoveSerializer
from src.item.models import Item
from src.item.serializers import ItemSerializer
from src.product.models import Product
from src.core.services_mixins import SerializerMixin, serialize_data, validate_serializer


def return_cart_items(request) -> ItemSerializer:
    """ Function for returning items from customer's cart """
    items = request.user.cart.items.all()
    serialized_items = ItemSerializer(items, many=True)
    return serialized_items


def clear_cart(request):
    """ Function for cleaning customer's cart """
    request.user.cart.items.all().delete()


class AddItemToCart:
    """ Class for add item to customer cart or update of quantity products in cart """
    def __init__(self, request):
        self.request = request

    def main(self) -> ItemSerializer:
        request_data_serializer = validate_serializer(serialize_data(serializer_class=CartProductAddSerializer, data=self.request.data))
        product = self.get_product(request_data_serializer)
        item = self.get_item(product)
        if not item.exists():
            item = self.create_item(product, request_data_serializer)
        else:
            item = self.update_item(item, request_data_serializer)
        return ItemSerializer(item)

    def get_product(self, request_data_serializer) -> Union[Product, exceptions.NotFound]:
        try:
            product = Product.objects.get(slug=request_data_serializer.data.get("product_slug"))
            return product
        except Product.DoesNotExist:
            return exceptions.NotFound("No such product.")

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
    """ Class for remove product to customer cart or update of quantity products in cart """
    def __init__(self, request):
        self.request = request

    def main(self) -> Optional[ItemSerializer]:
        request_data_serializer = serialize_data(serializer_class=CartProductRemoveSerializer, data=self.request.data)
        product_qty = self.pop_product_qty_from_reuqest_data(request_data_serializer)
        item = self.return_item_from_cart(request_data_serializer)
        if product_qty is not None:
            item = self.reduce_quantity_of_product(item, product_qty)
            return item
        else:
            self.remove_product(item)

    def pop_product_qty_from_reuqest_data(self, request_data_serializer) -> int:
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
            raise exceptions.NotFound("No such product.")

    def reduce_quantity_of_product(self, item, product_qty) -> ItemSerializer:
        item.update(quantity=F("quantity") - product_qty)
        if int(item[0].quantity) == 0:
            item[0].delete()
        return ItemSerializer(item[0])

    def remove_product(self, item):
        item[0].delete()
