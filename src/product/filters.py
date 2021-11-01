from django_filters import rest_framework as filters

from . import models


class ProductFilter(filters.FilterSet):
    """ Filter by price, category and available """
    max_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = models.Product
        fields = ("category", "available", "max_price", "min_price")
