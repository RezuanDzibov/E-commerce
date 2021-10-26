from django.urls import path
from . import views


app_name = "order"


urlpatterns = [
    path("create/", views.CreateOrder.as_view()),
    path("pay/", views.PayOrder.as_view())
]