from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.responses import GENERAL_AUTH_ERROR

User = get_user_model()


def validate_unique_email(email):
    """Validate that the email is not already in use."""
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError(GENERAL_AUTH_ERROR)


def validate_matching_passwords(password, confirmed_password):
    """Validate matching passwords."""
    if password != confirmed_password:
        raise serializers.ValidationError(GENERAL_AUTH_ERROR)