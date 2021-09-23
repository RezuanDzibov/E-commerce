from django.urls import path
from . import views


urlpatterns = [
    path("orders/", views.AddToOrder.as_view()),
    path("pay_order/", views.PayOrder.as_view())
]