from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from item.models import Item


Customer = get_user_model()


class Order(models.Model):
    delivery_statuses = (
        ("processed", "Processed"),
        ("delivering", "Delivering"),
        ("delivered", "Delivered")
    ) 
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    postal_code = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payed = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=10, choices=delivery_statuses)
    items = GenericRelation(Item, related_query_name="order")

    def __str__(self):
        return f"{self.customer}'s order status: {self.delivery_status}"

    @property
    def order_total_price(self):
        total_price = 0
        items = self.items.values("product__price", "quantity")
        for item in items:
            total_price += item["product__price"] * item["quantity"]
        return total_price

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"



