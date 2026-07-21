from email.mime.image import MIMEImage
from pathlib import Path
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

EMAIL_IMAGE_CID = "videoflix-email-image"
EMAIL_IMAGE_PATH = "auth_app/emails/mail.png"


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
    email = build_email(subject, plain_message, html_message, recipient)
    attach_email_image(email)
    email.send()


def build_email(subject, plain_message, html_message, recipient):
    """Build a multipart email with HTML alternative."""
    email = EmailMultiAlternatives(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
    )
    email.mixed_subtype = "related"
    email.attach_alternative(html_message, "text/html")
    return email


def render_auth_email(action_url, headline, message, button_text):
    """Render the auth email HTML template."""
    return render_to_string(
        "auth_app/emails/auth_email.html",
        {
            "action_url": action_url,
            "headline": headline,
            "message": message,
            "button_text": button_text,
            "image_cid": EMAIL_IMAGE_CID,
        },
    )


def attach_email_image(email):
    """Attach the inline email image."""
    image_path = finders.find(EMAIL_IMAGE_PATH)

    if not image_path:
        raise FileNotFoundError(f"Missing email image: {EMAIL_IMAGE_PATH}")

    image = MIMEImage(Path(image_path).read_bytes())
    image.add_header("Content-ID", f"<{EMAIL_IMAGE_CID}>")
    image.add_header("Content-Disposition", "inline", filename="mail.png")
    email.attach(image)