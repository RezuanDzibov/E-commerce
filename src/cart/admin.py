from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from src.item.models import Item
from .models import Cart


class ItemInline(GenericTabularInline):
    """Generic tabular inline for Item model."""
    model = Item
    fields = ("product", "quantity", "product_price", "total_price")
    readonly_fields = ("product", "product_price", "total_price")
    exclude = ('content_type', 'object_id',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (ItemInline,)
