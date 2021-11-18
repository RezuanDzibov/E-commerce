from rest_framework import serializers

from src.item.serializers import ItemSerializer
from src.order.serializers import OrderSerializer

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(read_only=True, many=True)
    cart_products = ItemSerializer(read_only=True, source='cart.items', many=True)

    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', 'orders', 'cart_products')