from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    product_slug = serializers.SlugField()
    product_qty = serializers.IntegerField(default=1, initial=1, min_value=1, max_value=10)


class CartRemoveSerializer(serializers.Serializer):
    product_slug = serializers.SlugField()
    product_qty = serializers.IntegerField(min_value=1, max_value=10, required=False)
