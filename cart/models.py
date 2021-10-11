from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from item.models import Item


Customer = get_user_model()


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart")
    items = GenericRelation(Item, related_query_name="cart")

    def __str__(self) -> str:
        return f"{self.customer}'s cart"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
