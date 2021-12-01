from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.CartProductItems.as_view()),
    path("clear/", views.ClearAllProductItemsFromCart.as_view()),
    path("add/", views.AddProductToCart.as_view()),
    path("remove/", views.RemoveProductItemFromCart.as_view()),
    path("reduce_quantity_of_product_item/", views.ReduceQuantityOfProductItem.as_view()),
]
