from django.urls import path

from src.order import views

app_name = "order"

urlpatterns = [
    path("", views.OrderList.as_view(), name="order-list"),
    path("<int:order_id>/", views.OrderRetrieve.as_view(), name="order-retrieve"),
    path("create/", views.OrderCreate.as_view(), name="order-create"),
    path("pay/<int:order_id>/", views.OrderPay.as_view(), name="order-pay"),
    path("update_delivery_status/<int:order_id>/", views.OrderStatusUpdate.as_view(), name="order-delivery_status-update")
]