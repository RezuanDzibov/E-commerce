from django.urls import path

from . import views


app_name = "cart"


urlpatterns = [
    path("items/", views.CartItems.as_view()),
    path("clear/", views.ClearCart.as_view()),
    path("add/", views.AddToCart.as_view()),
    path("remove/", views.RemoveFromCart.as_view()),
]
