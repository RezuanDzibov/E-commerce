from rest_framework import serializers


class CartProductAddSerializer(serializers.Serializer):
    """ Serializer for add item from customer cart """
    product_slug = serializers.SlugField()
    product_qty = serializers.IntegerField(default=1, initial=1, min_value=1, max_value=10)


class CartProductRemoveSerializer(serializers.Serializer):
    """ Serializer for remove item from customer cart """
    product_slug = serializers.SlugField()
    product_qty = serializers.IntegerField(min_value=1, max_value=10, required=False)
