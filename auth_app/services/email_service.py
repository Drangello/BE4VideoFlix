from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def build_frontend_url(page_path, uidb64, token):
    """Build a frontend URL with token parameters."""
    query = urlencode({"uid": uidb64, "token": token})
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


def build_logo_url():
    """Build the frontend logo URL for emails."""
    base_url = settings.FRONTEND_BASE_URL.rstrip("/")
    return f"{base_url}/EmailTemplates_Backend/Logo.svg"


def send_activation_email(user, uidb64, token):
    """Send account activation email."""
    activation_url = build_activation_url(uidb64, token)
    send_auth_email(
        subject="Activate your VideoFlix account",
        recipient=user.email,
        action_url=activation_url,
        headline="Activate your account",
        message="Please confirm your email address to start watching.",
        button_text="Activate account",
    )


def send_password_reset_email(user, uidb64, token):
    """Send password reset email."""
    reset_url = build_password_reset_url(uidb64, token)
    send_auth_email(
        subject="Reset your VideoFlix password",
        recipient=user.email,
        action_url=reset_url,
        headline="Reset your password",
        message="Choose a new password for your VideoFlix account.",
        button_text="Reset password",
    )


def send_auth_email(
    subject,
    recipient,
    action_url,
    headline,
    message,
    button_text,
):
    """Send a styled HTML auth email with plain text fallback."""
    plain_message = f"{message}\n\n{action_url}"
    html_message = render_auth_email(
        action_url,
        headline,
        message,
        button_text,
    )
    email = EmailMultiAlternatives(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()


def render_auth_email(action_url, headline, message, button_text):
    """Render the auth email HTML template."""
    return render_to_string(
        "auth_app/emails/auth_email.html",
        {
            "action_url": action_url,
            "headline": headline,
            "message": message,
            "button_text": button_text,
            "logo_url": build_logo_url(),
        },
    )