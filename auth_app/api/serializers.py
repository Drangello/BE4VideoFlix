from django.contrib.auth import authenticate

from rest_framework import serializers

from common.responses import GENERAL_AUTH_ERROR
from common.validators import (
    validate_matching_passwords,
    validate_unique_email,
)


class RegisterSerializer(serializers.Serializer):
    """Validate registration data."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        """Validate email uniqueness."""
        validate_unique_email(value)
        return value

    def validate(self, attrs):
        """Validate registration data."""
        validate_matching_passwords(
            attrs["password"],
            attrs["confirmed_password"],
        )
        return attrs


class LoginSerializer(serializers.Serializer):
    """Validate login credentials."""

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate the user."""
        user = authenticate(
            email=attrs["email"],
            password=attrs["password"],
        )

        if user is None:
            raise serializers.ValidationError(GENERAL_AUTH_ERROR)

        attrs["user"] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """Validate password reset data."""

    email = serializers.EmailField()


class PasswordConfirmSerializer(serializers.Serializer):
    """Validate a new password."""

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate matching passwords."""
        validate_matching_passwords(
            attrs["new_password"],
            attrs["confirm_password"],
        )
        return attrs