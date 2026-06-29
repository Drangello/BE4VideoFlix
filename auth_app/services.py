from django.contrib.auth import get_user_model

User = get_user_model()


def create_inactive_user(email, password):
    """Create an inactive user."""
    return User.objects.create_user(
        email=email,
        password=password,
        is_active=False,
    )