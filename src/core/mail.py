from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_delivery_status_by_mail(subject: str, order_id: int, delivery_status: str, receiver_email: str) -> None:
    send_mail(
        f"Hello {subject}!",
        f"""
        Hello! This message informs you about the delivery status of your order from ID: {order_id}.
        Status is: {delivery_status}
        """,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False
    )


def send_notify_about_order(subject, order_id, order_total_price, product_items_info, receiver_email):
    message = render_to_string("mail/order_info_message.html",
        {
            "order_id": order_id,
            "order_total_price": order_total_price,
            "product_items_info": product_items_info
        }
    )
    send_mail(
        f"Hello {subject}",
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False
    )