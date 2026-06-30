from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail


def build_activation_url(uidb64, token):
    """Build the frontend activation URL."""
    activation_path = f"/activate/{uidb64}/{token}/"

    return urljoin(
        settings.FRONTEND_BASE_URL,
        activation_path,
    )


def send_activation_email(user, uidb64, token):
    """Send account activation email."""
    activation_url = build_activation_url(uidb64, token)

    send_mail(
        subject="Activate your VideoFlix account",
        message=f"Activate your account here: {activation_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )