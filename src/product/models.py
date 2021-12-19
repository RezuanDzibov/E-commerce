from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


def get_upload_path(instance, filename):
    """Construct image path by product name and filename."""
    return f"product_images/{instance.product.name[:50]}/{filename}"


class Category(MPTTModel):
    """Category model."""
    name = models.CharField(max_length=300, verbose_name="Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Parent category"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"slug": self.slug})


class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=300, verbose_name="Name")
    slug = models.SlugField(unique=True, blank=True, help_text="You can leave it blank.", verbose_name="Slug")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Category")
    small_description = models.TextField(
        max_length=5000,
        blank=True,
        help_text="Small description about product",
        verbose_name="Small description"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    available = models.BooleanField(default=True, help_text="Is the product available", verbose_name="Available")
    created = models.DateTimeField(auto_now_add=True, help_text="Created date and time", verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, help_text="Updated date and time", verbose_name="Updated")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product:product-detail", kwargs={"slug": self.slug})


class Image(models.Model):
    """Image model."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_upload_path)
    alt_text = models.CharField(verbose_name="Alternative text", max_length=255, null=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        image_name = f"{self.image}".split('/')[-1]
        return f"{self.product.name} {image_name}"

    def get_absolute_url(self):
        return reverse("image-detail", kwargs={"pk": self.pk})
