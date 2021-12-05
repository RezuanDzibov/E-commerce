from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.ProductItems.as_view()),
    path("clear/", views.ClearCart.as_view()),
    path("add/<slug:product_slug>/", views.ProductItemAddToCart.as_view()),
    path("remove/<slug:product_slug>/", views.ProductItemRemoveFromCart.as_view()),
    path("reduce_quantity/<slug:product_slug>/", views.ProductItemReduceQuantity.as_view()),
]
