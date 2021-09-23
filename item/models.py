from django.db import models
from product.models import Product
from django.core import validators
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Item(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    product = models.ForeignKey(Product, related_name="product_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} {self.quantity}"

    @property
    def item_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
