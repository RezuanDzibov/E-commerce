from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("items/", views.CartProducts.as_view()),
    path("clear/", views.ClearAllProductsFromCart.as_view()),
    path("add/", views.AddProductToCart.as_view()),
    path("remove/", views.RemoveProductFromCart.as_view()),
]
