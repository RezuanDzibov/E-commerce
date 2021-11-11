from django.core.mail import send_mail
from django.conf import settings


def send_delivery_status_by_mail(subject, order_id, delivery_status, receiver_email):
    send_mail(
        f"Hello {subject}!",
        f"""
        Hello! This message informs you about the delivery status of your order from ID:{order_id}."
        Status is: {delivery_status}
        """,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False
    )