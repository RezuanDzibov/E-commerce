from . import models
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    max_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = models.Product
        fields = ("category", "available", "max_price", "min_price")