from typing import Optional

from cart.serializers import CartAddSerializer, CartRemoveSerializer

from django.db.models import F

from rest_framework import exceptions

from item.models import Item
from item.serializers import ItemSerializer

from product.models import Product

from utils.services_mixins import SerializerMixin


def return_cart_items(request) -> ItemSerializer:
    items = request.user.cart.items.all()
    serializerd_items = ItemSerializer(items, many=True)
    return serializerd_items


def clear_cart(request):
    request.user.cart.items.all().delete()


class AddToCart(SerializerMixin):
    serializer_class = CartAddSerializer

    def __init__(self, request):
        self.request = request

    def main(self) -> ItemSerializer:
        self.serializer = self.serialize(data=self.request.data)
        self.product = self.get_product()
        self.item = self.get_item()
        if not self.item.exists():
            item = self.create_item()
        else:
            item = self.update_item()
        return ItemSerializer(item)

    def get_product(self) -> Product:
        try:
            product = Product.objects.get(slug=self.serializer.data["product_slug"])
            return product
        except Product.DoesNotExist:
            return exceptions.NotFound("No such product.")

    def get_item(self) -> Item:
        item = Item.objects.filter(cart__id=self.request.user.cart.id, product=self.product)
        return item

    def create_item(self) -> Item:
        item = Item.objects.create(
            content_object=self.request.user.cart,
            product=self.product,
            quantity=self.serializer.data["product_qty"]
        )
        return item

    def update_item(self) -> Item:
        self.item.update(quantity=F("quantity") + self.serializer.data["product_qty"])
        return self.item[0]


class RemoveFromCart(SerializerMixin):
    serializer_class = CartRemoveSerializer

    def __init__(self, request):
        self.request = request

    def main(self) -> Optional[ItemSerializer]:
        self.serializer = self.serialize(self.request.data)
        self.product_qty = self.return_product_qty()
        self.item = self.return_item()
        if self.product_qty is not None:
            item = self.reduce()
            return item
        else:
            self.remove()

    def return_product_qty(self) -> int:
        product_qty = self.serializer.data.get("product_qty", None)
        return product_qty

    def return_item(self) -> Item:
        item = Item.objects.filter(
            cart__id=self.request.user.cart.id,
            product__slug=self.serializer.data["product_slug"]
        )
        if item.exists():
            return item
        else:
            raise exceptions.NotFound("No such product.")

    def reduce(self) -> ItemSerializer:
        self.item.update(quantity=F("quantity") - self.product_qty)
        if int(self.item[0].quantity) == 0:
            self.item[0].delete()
        return ItemSerializer(self.item[0])

    def remove(self):
        self.item[0].delete()
