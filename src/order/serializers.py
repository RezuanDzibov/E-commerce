from rest_framework import serializers

from src.item.serializers import ItemSerializer
from src.order.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "address", "city", "postal_code")


class OrderCreateDataInputSerializer(OrderCreateSerializer):
    product_item_id_list = serializers.ListField(child=serializers.IntegerField(min_value=0))

    class Meta:
        model = Order
        fields = OrderCreateSerializer.Meta.fields + ('product_item_id_list',)


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
