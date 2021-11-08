from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """ Item Serializer """
    name = serializers.CharField(source="product.name")
    quantity = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Item
        fields = ("id", "name", "product_price", "total_price", "quantity")