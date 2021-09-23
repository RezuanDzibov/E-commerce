from rest_framework import viewsets, mixins, filters, pagination
from . import models, serializers
from . import permssions as app_permissions
from . import filters as app_filters
from utils import view_mixins
from django_filters import rest_framework as django_filters


class CategoryViewSet(view_mixins.SerializerByAction, viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    default_serializer_class = serializers.CategoryCreateUpdateSerializer
    serializer_classes = {
        "list": serializers.CategotyListSerializer,
        "retrieve": serializers.CategoryRetriveSerializer
    }
    lookup_field = "slug"
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("name",)
    permission_classes = (app_permissions.IsStaffOrReadOnly,)
    pagination_class = pagination.PageNumberPagination 
    


class ProductViewSet(view_mixins.SerializerByAction, viewsets.ModelViewSet):
    queryset = models.Product.objects.filter(available=True)
    default_serializer_class = serializers.ProductCreateUpdateSerializer
    serializer_classes = {
        "list": serializers.ProductListSerializer, 
        "retrieve": serializers.ProductRetriveSerializer
    }
    lookup_field = "slug"
    permission_classes = (app_permissions.IsStaffOrReadOnly,)
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = app_filters.ProductFilter
    search_fields = ("name", "category__name", "price")


class ImageViewSet(
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin, 
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    permission_classes = (app_permissions.IsStaffOrReadOnly,)
    pagination_class = None