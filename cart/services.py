from rest_framework.exceptions import ValidationError
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


def remove_from_cart(request):
    serializer = CartRemoveSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        product_qty = serializer.data.get("product_qty", None)
        items = Item.objects.filter(cart__id=request.user.cart.id, product__slug=serializer.data["product_slug"])
        if items.exists():
            item = items[0]
            if product_qty is not None and isinstance(int(product_qty), int):
                items.update(quantity=F("quantity") - product_qty)
                if int(items[0].quantity) == 0:
                    item.delete()
                return ItemSerializer(items[0])
            else:
                item.delete()
        else:
            raise ValidationError("You don't have so product in your cart.")