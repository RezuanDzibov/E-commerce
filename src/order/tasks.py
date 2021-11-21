from config.celery import app
from src.core.mail import send_delivery_status_by_mail, send_notify_about_order


@app.task
def send_delivery_status(subject, order_id, delivery_status, receiver_email):
    send_delivery_status_by_mail(subject, order_id, delivery_status, receiver_email)


@app.task
def send_notify(subject, order_id, order_total_price, product_items_info, receiver_email):
    send_notify_about_order(subject, order_id, order_total_price, product_items_info, receiver_email)