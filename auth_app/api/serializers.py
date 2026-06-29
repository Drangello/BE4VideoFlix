from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth_app.utils import get_general_error_message

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """Validate registration data."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(get_general_error_message())

        return value

    def validate(self, attrs):
        """Validate matching passwords."""
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError(get_general_error_message())

        return attrs
