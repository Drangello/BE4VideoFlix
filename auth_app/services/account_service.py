import django_rq

from auth_app.services.token_service import (
    create_activation_data,
    create_password_reset_data,
    get_user_id_from_uid,
    is_valid_token,
)
from auth_app.services.user_service import (
    activate_user,
    create_inactive_user,
    get_user_by_email,
    get_user_by_id,
    set_user_password,
)
from auth_app.tasks import (
    send_activation_email_task,
    send_password_reset_email_task,
)


def register_account(email, password):
    """Create an inactive account and queue its activation email."""
    user = create_inactive_user(email=email, password=password)
    activation_data = create_activation_data(user)
    django_rq.get_queue("emails").enqueue(
        send_activation_email_task,
        user.id,
        activation_data["uidb64"],
        activation_data["token"],
    )
    return user, activation_data


def activate_account(uidb64, token):
    """Activate the account identified by a valid token."""
    try:
        user = get_user_from_uid(uidb64)
    except Exception:
        return False

    if not user or not is_valid_token(user, token):
        return False

    activate_user(user)
    return True


def request_password_reset(email):
    """Queue a password reset email for an active account."""
    user = get_user_by_email(email)
    if not user or not user.is_active:
        return

    reset_data = create_password_reset_data(user)
    django_rq.get_queue("emails").enqueue(
        send_password_reset_email_task,
        user.id,
        reset_data["uidb64"],
        reset_data["token"],
    )


def confirm_password_reset(uidb64, token, new_password):
    """Set a new password when the reset token is valid."""
    user = get_user_from_uid(uidb64)
    if not user or not is_valid_token(user, token):
        return False

    set_user_password(user, new_password)
    return True


def get_user_from_uid(uidb64):
    """Return a user decoded from uidb64, if one exists."""
    try:
        user_id = get_user_id_from_uid(uidb64)
    except Exception:
        return None

    return get_user_by_id(user_id)
