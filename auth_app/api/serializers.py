from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "confirmed_password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        """Validate email uniqueness."""

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Bitte überprüfe deine Eingaben und versuche es erneut."
            )

        return value

    def validate(self, attrs):
        """Validate matching passwords."""

        password = attrs.get("password")
        confirmed = attrs.get("confirmed_password")

        if password != confirmed:
            raise serializers.ValidationError(
                "Bitte überprüfe deine Eingaben und versuche es erneut."
            )

        return attrs

    def create(self, validated_data):
        """Create inactive user."""

        validated_data.pop("confirmed_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,
        )

        return user
