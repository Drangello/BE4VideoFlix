from rest_framework.views import APIView

from auth_app.api.serializers import RegisterSerializer
from auth_app.services.email_service import send_activation_email
from auth_app.services.token_service import create_activation_data
from auth_app.services.user_service import create_inactive_user
from common.responses import created_response


class RegisterView(APIView):
    """Handle user registration."""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_inactive_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        activation_data = create_activation_data(user)

        send_activation_email(
            user=user,
            uidb64=activation_data["uidb64"],
            token=activation_data["token"],
        )

        return created_response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "token": activation_data["token"],
            }
        )
