from config.celery import app
from src.core.mail import send_delivery_status_by_mail


@app.task
def send_delivery_status(subject, order_id, delivery_status, receiver_email):
    send_delivery_status_by_mail(subject, order_id, delivery_status, receiver_email)