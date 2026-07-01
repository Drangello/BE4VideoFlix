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
    return User.objects.filter(email=email).first()


def get_user_by_id(user_id):
    """Return a user by id."""
    return User.objects.filter(pk=user_id).first()


def activate_user(user):
    """Activate a user account."""
    user.is_active = True
    user.save(update_fields=["is_active"])


def set_user_password(user, password):
    """Set and save a user's password."""
    user.set_password(password)
    user.save(update_fields=["password"])