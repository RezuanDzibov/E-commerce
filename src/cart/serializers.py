from rest_framework import serializers


class CartProductItem(serializers.Serializer):
    product_slug = serializers.SlugField()


class CartProductItemAddSerializer(CartProductItem):
    product_qty = serializers.IntegerField(default=1, initial=1, min_value=1, max_value=10)


class CartProductItemRemoveSerializer(CartProductItem):
    pass


class CartProductItemReduceSerializer(CartProductItem):
    product_qty = serializers.IntegerField(default=1, initial=1, min_value=1, max_value=10)
