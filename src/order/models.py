from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from src.item.models import Item


Customer = get_user_model()


class Order(models.Model):
    delivery_statuses = (
        ("unpaid", "Unpaid"),
        ("processing", "Processing"),
        ("delivering", "Delivering"),
        ("delivered", "Delivered")
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", verbose_name="Customer")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    phone = PhoneNumberField(verbose_name="Phone Number")
    address = models.CharField(max_length=300, verbose_name="Address")
    city = models.CharField(max_length=300, verbose_name="City")
    postal_code = models.BigIntegerField(verbose_name="Postal Code")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created date and time")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated date and time")
    paid = models.BooleanField(default=False, verbose_name="Is paid")
    delivery_status = models.CharField(
        max_length=10,
        choices=delivery_statuses,
        verbose_name="Delivery status",
        default="unpaid"
    )
    items = GenericRelation(Item, related_query_name="order", verbose_name="Products")

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.customer}'s order status: {self.delivery_status}"

    @property
    def order_total_price(self):
        """Instance total price."""
        total_price = 0
        items = self.items.values("product__price", "quantity")
        for item in items:
            total_price += item["product__price"] * item["quantity"]
        return total_price
