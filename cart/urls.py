from django.urls import path
from . import views


urlpatterns = [
    path("items/", views.CartItems.as_view()),
    path("clear/", views.ClearCart.as_view()),
    path("add/", views.AddToCart.as_view()),
    path("remove/", views.RemoveFromCart.as_view()),
]
