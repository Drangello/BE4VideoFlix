from django.contrib.auth import get_user_model

User = get_user_model()


def create_inactive_user(email, password):
    """Create a new inactive user."""

    return User.objects.create_user(
        email=email,
        password=password,
        is_active=False,
    )


def get_user_by_email(email):
    """Return a user by email."""

    return User.objects.filter(
        email=email,
    ).first()