from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, pagination, viewsets

from src.core.mixins import SerializerByActionMixin
from src.core.permssions import IsStaffOrReadOnly

from . import filters as app_filters
from . import models
from . import serializers


class CategoryViewSet(SerializerByActionMixin, viewsets.ModelViewSet):
    """ Category ViewSet """
    queryset = models.Category.objects.all()
    default_serializer_class = serializers.CategoryCreateUpdateSerializer
    serializer_classes = {
        "list": serializers.CategoryListSerializer,
        "retrieve": serializers.CategoryRetrieveSerializer
    }
    lookup_field = "slug"
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name",)
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = pagination.PageNumberPagination


class ProductViewSet(SerializerByActionMixin, viewsets.ModelViewSet):
    """ Product ViewSet """
    queryset = models.Product.objects.all()
    default_serializer_class = serializers.ProductCreateUpdateSerializer
    serializer_classes = {
        # "list": serializers.ProductListSerializer,
        "retrieve": serializers.ProductRetrieveSerializer
    }
    lookup_field = "slug"
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = app_filters.ProductFilter
    search_fields = ("name", "category__name", "price")


class ImageViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """ Image ViewSet """
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = None
