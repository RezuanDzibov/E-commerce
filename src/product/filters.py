from django_filters import rest_framework as filters

from src.product import models


class ProductFilter(filters.FilterSet):
    """Filter by price, category and available flag."""
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = models.Product
        fields = ("category", "available", "max_price", "min_price")
