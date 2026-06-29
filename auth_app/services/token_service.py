from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def create_activation_data(user):
    """Create uid and token for account activation."""

    return {
        "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }


def get_user_id_from_uid(uidb64):
    """Decode uidb64 and return user id."""

    return force_str(urlsafe_base64_decode(uidb64))


def is_valid_token(user, token):
    """Return whether the given token is valid for the user."""

    return default_token_generator.check_token(user, token)
