from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("", views.OrderList.as_view()),
    path("<int:order_id>/", views.OrderRetrieve.as_view()),
    path("create/", views.OrderCreate.as_view()),
    path("pay/<int:order_id>/", views.OrderPay.as_view()),
    path("update_delivery_status/<int:order_id>/", views.OrderStatusUpdate.as_view())
]