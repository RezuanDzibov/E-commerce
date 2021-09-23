from .models import Order
from rest_framework import serializers
from item.serializers import ItemSerializer


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


class PayOrder(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
