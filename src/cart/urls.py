from django.urls import path

from src.cart import views

app_name = "cart"

urlpatterns = [
    path("", views.ProductItemList.as_view(), name="product_items-list"),
    path("clear/", views.ClearCart.as_view(), name="clear-cart"),
    path("add/<slug:product_slug>/", views.ProductItemAddToCart.as_view(), name="product_item-add"),
    path("remove/<slug:product_slug>/", views.ProductItemRemoveFromCart.as_view(), name="product_item-remove"),
    path("reduce_quantity/<slug:product_slug>/", views.ProductItemReduceQuantity.as_view(), name="product_item-reduce"),
]
