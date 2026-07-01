from auth_app.services.email_service import (
    send_activation_email,
    send_password_reset_email,
)
from auth_app.services.user_service import get_user_by_id


def send_activation_email_task(user_id, uidb64, token):
    """Send activation email in the background."""
    user = get_user_by_id(user_id)

    if user:
        send_activation_email(user, uidb64, token)


def send_password_reset_email_task(user_id, uidb64, token):
    """Send password reset email in the background."""
    user = get_user_by_id(user_id)

    if user:
        send_password_reset_email(user, uidb64, token)