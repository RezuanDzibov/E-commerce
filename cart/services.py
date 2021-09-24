from cart.serializers import CartAddSerializer, CartRemoveSerializer
from product.models import Product
from item.models import Item
from django.db.models import F
from item.serializers import ItemSerializer


def return_cart_items(request):
    items = request.user.cart.items.all()
    serializerd_items = ItemSerializer(items, many=True)
    return serializerd_items


def clear_cart(request):
    request.user.cart.items.all().delete()


def add_to_cart(request):
    serializer = CartAddSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        product = Product.objects.get(slug=serializer.data["product_slug"])
        items = Item.objects.filter(cart__id=request.user.cart.id, product=product)
        if not items.exists():
            item = Item.objects.create(
                content_object=request.user.cart, 
                product=product, 
                quantity=serializer.data["product_qty"]
            )
            return ItemSerializer(item)
        items.update(quantity=F("quantity") + serializer.data["product_qty"])
        return items[0]


class RemoveFromCart:
    def __init__(self, request):
        self.request = request

    def main(self):
        serializered_object = self.validate_input_data()
        self.product_qty = self.return_product_qty(serializered_object)
        self.items = self.return_items(serializered_object)
        removed = self.reduce_or_remove()
        return removed 

    def validate_input_data(self):
        serializer = CartRemoveSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            return serializer
    
    def return_product_qty(self, serializer):
        product_qty = serializer.data.get("product_qty", None)
        return product_qty

    def return_items(self, serializer):
        items = Item.objects.filter(cart__id=self.request.user.cart.id, product__slug=serializer.data["product_slug"])
        return items

    def reduce_or_remove(self):
        if self.items.exists():
            item = self.items[0]
            if self.product_qty is not None and isinstance(self.product_qty, int):
                self.items.update(quantity=F("quantity") - self.product_qty)
                if int(self.items[0].quantity) == 0:
                    item.delete()
                return ItemSerializer(self.items[0])
            else:
                item.delete()
        raise Exception("You do not have such item in your cart")


# def remove_from_cart(request):
#     serializer = CartRemoveSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         product_qty = serializer.data.get("product_qty", None)
#         items = Item.objects.filter(cart__id=request.user.cart.id, product__slug=serializer.data["product_slug"])
#         if items.exists():
#             item = items[0]
#             if product_qty is not None and isinstance(int(product_qty), int):
#                 items.update(quantity=F("quantity") - product_qty)
#                 if int(items[0].quantity) == 0:
#                     item.delete()
#                 return ItemSerializer(items[0])
#             else:
#                 item.delete()
#         else:
#             raise Exception("You don't have so product in your cart.")