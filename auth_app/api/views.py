import django_rq
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import RegisterSerializer
from auth_app.services.token_service import (
    get_user_id_from_uid,
    is_valid_token,
)
from auth_app.services.token_service import create_activation_data
from auth_app.services.user_service import (
    activate_user,
    create_inactive_user,
    get_user_by_id,
)
from auth_app.tasks import send_activation_email_task
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

        django_rq.enqueue(
            send_activation_email_task,
            user.id,
            activation_data["uidb64"],
            activation_data["token"],
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


class ActivateView(APIView):
    """Activate a user account."""

    def get(self, request, uidb64, token):
        try:
            user_id = get_user_id_from_uid(uidb64)
            user = get_user_by_id(user_id)
        except Exception:
            return self.get_error_response()

        if not user or not is_valid_token(user, token):
            return self.get_error_response()

        activate_user(user)

        return Response(
            {"message": "Account successfully activated."},
            status=status.HTTP_200_OK,
        )

    def get_error_response(self):
        return Response(
            {"message": "Activation failed."},
            status=status.HTTP_400_BAD_REQUEST,
        )