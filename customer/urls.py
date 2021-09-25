from django.urls import path
from . import views


urlpatterns = [
    path("", views.CustomerCartAndOrders.as_view()),
]
