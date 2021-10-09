from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available")
    list_filter = ("category", "available")
    

@admin.register(models.Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ("name", "parent", "indented_title", "tree_actions",)
    mptt_level_indent = 20


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    pass