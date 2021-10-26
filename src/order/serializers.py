from rest_framework import serializers
from src.item.serializers import ItemSerializer

from .models import Order


class ItemIDsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(min_value=0))


class AddtoOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "address", "city", "postal_code")


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name", 
            "last_name", 
            "phone", 
            "address", 
            "city", 
            "postal_code",
            "payed",
            "delivery_status",
            "items"
        )


class PayOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
