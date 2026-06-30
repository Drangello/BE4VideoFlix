from django.contrib.auth import get_user_model

from auth_app.services.email_service import send_activation_email

User = get_user_model()


def send_activation_email_task(user_id, uidb64, token):
    """Send activation email in background."""
    user = User.objects.get(pk=user_id)

    send_activation_email(
        user=user,
        uidb64=uidb64,
        token=token,
    )