from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken


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
    """Return whether the given token is valid."""
    return default_token_generator.check_token(user, token)


def create_token_pair(user):
    """Create access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def set_auth_cookies(response, token_pair):
    """Set access and refresh token cookies."""
    set_access_cookie(response, token_pair["access"])
    set_refresh_cookie(response, token_pair["refresh"])


def set_access_cookie(response, token):
    """Set the access token cookie."""
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="Lax",
        max_age=get_token_max_age("ACCESS_TOKEN_LIFETIME"),
    )


def set_refresh_cookie(response, token):
    """Set the refresh token cookie."""
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="Lax",
        max_age=get_token_max_age("REFRESH_TOKEN_LIFETIME"),
    )


def get_token_max_age(setting_name):
    """Return a token lifetime in seconds."""
    return int(settings.SIMPLE_JWT[setting_name].total_seconds())
