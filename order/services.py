from rest_framework.validators import ValidationError
from cart.models import Item
from .models import Order
from .serializers import OrderSerializer, AddtoOrderSerializer, PayOrder


def return_orders(request):
    orders = Order.objects.filter(customer=request.user)
    serializered_orders = OrderSerializer(orders, many=True)
    return serializered_orders


def add_to_order(request):
    data = request.data.copy()
    try:
        data_ids = data.pop("ids")[0].split(",")
        ids = []
        for id in data_ids:
            if not isinstance(int(id), int):
                raise ValidationError("You have provided invalid data for the ids field.")
            ids.append(int(id))  
        serializer = AddtoOrderSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            order = Order.objects.create(
                customer=request.user, 
                **serializer.validated_data, 
                delivery_status="processed"
            )     
        items = Item.objects.filter(id__in=ids, cart__id=request.user.cart.id)
        if items.exists():
            for item in items:
                item.content_object = order
                item.save()
            return OrderSerializer(order)
        else:
            raise ValidationError("You don't have so items in your cart")
    except KeyError:
        raise ValidationError("You have not filled in the ids field")
   

def pay(request):
    serializer = PayOrder(data=request.data)
    if serializer.is_valid(raise_exception=True):
        order_id=serializer.data["id"]
        try:
            order = Order.objects.get(customer=request.user, id=order_id, payed=False)
            order.payed = True
            order.save()
            serializerd_order = OrderSerializer(order)
            return serializerd_order
        except Order.DoesNotExist:
            return None
        
