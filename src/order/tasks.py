from decimal import Decimal

from config.celery import app
from src.core.mail import send_delivery_status_by_mail, send_notify_about_order


@app.task
def send_delivery_status(subject: str, order_id: int, delivery_status: str, receiver_email: str) -> None:
    """
    @param subject: Customer first and last name.
    @param order_id: Order model instance id.
    @param delivery_status: Order model instance delivery status.
    @param receiver_email: Customer email.
    """
    send_delivery_status_by_mail(subject, order_id, delivery_status, receiver_email)


@app.task
def send_notify(
        subject: str,
        order_id: int,
        order_total_price: Decimal,
        product_items_info: list,
        receiver_email: str
) -> None:
    """
    @param subject: Customer first and last name.
    @param order_id: Order model instance id.
    @param order_total_price: Order model instance total price.
    @param product_items_info: product item info.
    @param receiver_email: Customer email.
    """
    send_notify_about_order(subject, order_id, order_total_price, product_items_info, receiver_email)