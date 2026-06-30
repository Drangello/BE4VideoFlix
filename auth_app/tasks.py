from auth_app.services.email_service import send_activation_email


def send_activation_email_task(user, uidb64, token):
    """Background task for sending activation emails."""
    send_activation_email(user, uidb64, token)