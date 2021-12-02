from drf_yasg import openapi
from rest_framework import serializers

from src.item.serializers import ItemSerializer

from .models import Order


class CreateOrderSerializer(serializers.ModelSerializer):

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
            "paid",
            "delivery_status",
            "items"
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["product_items"] = representation.pop("items")
        return representation


class OrderStatusUpdateSerializer(serializers.Serializer):
    delivery_status = serializers.ChoiceField(choices=Order.delivery_statuses)
