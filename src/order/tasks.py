from decimal import Decimal

from config.celery import app
from src.core.mail import send_delivery_status_by_mail, send_notify_about_order


@app.task
def send_delivery_status(subject: str, order_id: int, delivery_status: str, receiver_email: str) -> None:
    send_delivery_status_by_mail(subject, order_id, delivery_status, receiver_email)


@app.task
def send_notify(
        subject: str,
        order_id: int,
        order_total_price: Decimal,
        product_items_info: list,
        receiver_email: str
) -> None:
    send_notify_about_order(subject, order_id, order_total_price, product_items_info, receiver_email)