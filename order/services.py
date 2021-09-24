from cart.models import Item
from .models import Order
from .serializers import OrderSerializer, AddtoOrderSerializer, PayOrder


def return_orders(request):
    orders = Order.objects.filter(customer=request.user)
    serializered_orders = OrderSerializer(orders, many=True)
    return serializered_orders


# def add_to_order(request):
#     data = request.data.copy()
#     try:
#         data_ids = data.pop("ids")[0].split(",")
#         ids = []
#         for id in data_ids:
#             if not isinstance(id, int):
#                 raise Exception("You have provided invalid data for the ids field.")
#             ids.append(int(id))    
#         items = Item.objects.filter(id__in=ids, cart__id=request.user.cart.id)
#         if items.exists():
#             serializer = AddtoOrderSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 order = Order.objects.create(
#                 customer=request.user, 
#                 **serializer.validated_data, 
#                 delivery_status="processed"
#                 )   
#             for item in items:
#                 item.content_object = order
#                 item.save()
#             return OrderSerializer(order)
#         else:
#             raise ValidationError("You don't have so items in your cart")
#     except KeyError:
#         raise ValidationError("You have not filled in the ids field")


class AddToOrder:
    def __init__(self, request):
        self.request = request
        self.data = request.data.copy()

    def main(self):
        ids = self.filter_ids()
        items = self.return_items(ids)
        order = self.create_order()
        self.add_item_to_order(order, items)
        return OrderSerializer(order)
    
    def filter_ids(self):
        data_ids = self.data.pop("ids")[0].split(",")
        ids = []
        invalid_ids = []
        for id in data_ids:
            try:
                ids.append(int(id))
            except Exception as ex:
                invalid_ids.append(id)
        if invalid_ids.count() > 0:
            raise Exception(f"You have provided invalid data for the ids field.{invalid_ids}")
        return ids

    def create_order(self):
        serializer = AddtoOrderSerializer(data=self.data)
        if serializer.is_valid(raise_exception=True):
            order = Order.objects.create(
                customer=self.request.user, 
                **serializer.validated_data, 
                delivery_status="processed"
            )   
            return order

    def add_item_to_order(self, order, items):
        for item in items:
            item.content_object = order
            item.save()
        return 

    def return_items(self, ids):
        items = Item.objects.filter(id__in=ids, cart__id=self.request.user.cart.id)
        if items.exists():
            return items
        raise Exception("You don't have so items in your cart")
   

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
            return Exception("You do not have such an order.")
        
