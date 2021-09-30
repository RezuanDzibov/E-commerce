from rest_framework import exceptions
from cart.serializers import CartAddSerializer, CartRemoveSerializer
from product.models import Product
from item.models import Item
from django.db.models import F
from item.serializers import ItemSerializer
from utils.services_mixins import SerializerMixin


def return_cart_items(request):
    items = request.user.cart.items.all()
    serializerd_items = ItemSerializer(items, many=True)
    return serializerd_items


def clear_cart(request):
    request.user.cart.items.all().delete()


class AddToCart(SerializerMixin):
    serializer_class = CartAddSerializer

    def __init__(self, request):
        self.request = request

    def main(self):
        self.serializer = self.serialize(data=self.request.data)
        self.product = self.get_product()
        self.item = self.get_item()
        if not self.item.exists():
            item = self.create_item()
        else:
            item = self.update_item()
        return ItemSerializer(item)

    def get_product(self):
        try:
            product = Product.objects.get(slug=self.serializer.data["product_slug"])
            return product
        except Product.DoesNotExist:
            return exceptions.NotFound("No such product.")
    
    def get_item(self):
        item = Item.objects.filter(cart__id=self.request.user.cart.id, product=self.product)
        return item

    def create_item(self):
        item = Item.objects.create(content_object=self.request.user.cart, product=self.product, quantity=self.serializer.data["product_qty"])
        return item

    def update_item(self):
        self.item.update(quantity=F("quantity") + self.serializer.data["product_qty"])
        return self.item[0]


class RemoveFromCart(SerializerMixin):
    serializer_class = CartRemoveSerializer

    def __init__(self, request):
        self.request = request    

    def main(self):
        self.serializer = self.serialize(self.request.data)
        self.product_qty = self.return_product_qty()
        self.item = self.return_item()
        if self.product_qty is not None: 
            item = self.reduce()
            return item
        else:
            self.remove()
    
    def return_product_qty(self):
        product_qty = self.serializer.data.get("product_qty", None)
        return product_qty

    def return_item(self):
        item = Item.objects.filter(cart__id=self.request.user.cart.id, product__slug=self.serializer.data["product_slug"])
        if item.exists():
            return item
        else:
            raise exceptions.NotFound("No such product.")

    def reduce(self):
        self.item.update(quantity=F("quantity") - self.product_qty)
        if int(self.item[0].quantity) == 0:
            self.item[0].delete()
            return None
        return ItemSerializer(self.item[0])

    def remove(self):
        self.item[0].delete()
