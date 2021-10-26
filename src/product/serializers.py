from rest_framework import serializers
from . import models


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    url = serializers.HyperlinkedIdentityField(view_name="product:product-detail", lookup_field="slug", read_only=True)

    class Meta:
        model = models.Product
        fields = ("name", "slug", "category", "price", "available", "url")


class ProductRetriveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    images = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="product:image-detail")

    class Meta:
        model = models.Product
        fields = (
            "name", 
            "slug", 
            "category", 
            "price", 
            "available", 
            "small_descpription", 
            "created", 
            "updated",
            "images"
        )


class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = (
            "name", 
            "slug", 
            "category", 
            "small_descpription", 
            "price", 
            "available"
        )


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ("image", "alt_text")


class CategotyListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="product:category-detail", lookup_field="slug")

    class Meta:
        model = models.Category
        fields = ("name", "url")


class CategoryRetriveSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True)

    class Meta:
        model = models.Category
        fields = ("name", "slug", "parent", "products")


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ("name", "parent")
