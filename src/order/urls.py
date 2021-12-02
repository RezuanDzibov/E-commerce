from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("", views.GetOrders.as_view()),
    path("<int:order_id>/", views.GetOrder.as_view()),
    path("create/", views.CreateOrder.as_view()),
    path("pay/<int:order_id>/", views.PayOrder.as_view()),
    path("update_delivery_status/<int:order_id>/", views.UpdateOrderStatus.as_view())
]