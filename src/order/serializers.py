from rest_framework import serializers

from src.item.serializers import ItemSerializer

from .models import Order


class AddToOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "address", "city", "postal_code")


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "order_id",
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
        products = representation.pop("items")
        representation["products"] = products
        return representation


class PayOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)


class OrderStatusUpdateSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)
    delivery_status = serializers.ChoiceField(choices=Order.delivery_statuses)
