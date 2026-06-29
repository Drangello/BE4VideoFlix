from rest_framework import serializers

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
