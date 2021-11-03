from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from src.product.models import Product


class Item(models.Model):
    """ Item model with polymorphic relationship to Order, Cart """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    product = models.ForeignKey(Product, related_name="product_items", on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.product.name} {self.quantity}"

    @property
    def product_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.quantity
