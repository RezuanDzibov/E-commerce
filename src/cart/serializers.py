from rest_framework import serializers


class CartProductItem(serializers.Serializer):
    product_qty = serializers.IntegerField(default=1, initial=1, min_value=1, max_value=10)