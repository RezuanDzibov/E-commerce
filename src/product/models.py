from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.urls import reverse


def get_upload_path(instance, filename):
    return f"product_images/{instance.product.name[:50]}/{filename}"


class Category(MPTTModel):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="children")
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"slug": self.slug})


class Product(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, help_text="You can leave it blank.")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    small_descpription = models.TextField(max_length=5000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})
        

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_upload_path)
    alt_text = models.CharField(verbose_name="Alturnative text", max_length=255, null=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        image_name = f"{self.image}".split('/')[-1]
        return f"{self.product.name} {image_name}"
    
    def get_absolute_url(self):
        return reverse("image-detail", kwargs={"pk": self.pk})