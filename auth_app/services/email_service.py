from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail


def build_frontend_url(page_path, uidb64, token):
    """Build a frontend URL with token parameters."""
    query = urlencode(
        {
            "uid": uidb64,
            "token": token,
        }
    )
    base_url = settings.FRONTEND_BASE_URL.rstrip("/")
    return f"{base_url}/{page_path}?{query}"


def build_activation_url(uidb64, token):
    """Build the frontend activation URL."""
    return build_frontend_url(
        "pages/auth/activate.html",
        uidb64,
        token,
    )


def build_password_reset_url(uidb64, token):
    """Build the frontend password reset URL."""
    return build_frontend_url(
        "pages/auth/confirm_password.html",
        uidb64,
        token,
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


def send_password_reset_email(user, uidb64, token):
    """Send password reset email."""
    reset_url = build_password_reset_url(uidb64, token)

    send_mail(
        subject="Reset your VideoFlix password",
        message=f"Reset your password here: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )