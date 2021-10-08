from django.urls import path
from . import views


app_name = "order"


urlpatterns = [
    path("add/", views.AddToOrder.as_view()),
    path("pay/", views.PayOrder.as_view())
]