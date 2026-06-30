import django_rq
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from auth_app.api.serializers import LoginSerializer, RegisterSerializer
from auth_app.services.token_service import (
    create_access_token,
    create_activation_data,
    create_token_pair,
    get_user_id_from_uid,
    is_valid_token,
    set_access_cookie,
    set_auth_cookies,
    blacklist_refresh_token,
    delete_auth_cookies,
)
from auth_app.services.user_service import (
    activate_user,
    create_inactive_user,
    get_user_by_id,
)
from auth_app.tasks import send_activation_email_task
from common.responses import created_response, ok_response


class RegisterView(APIView):
    """Handle user registration."""

    authentication_classes = []
    permission_classes = [AllowAny]

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

    authentication_classes = []
    permission_classes = [AllowAny]

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


class LoginView(APIView):
    """Authenticate a user and set JWT cookies."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token_pair = create_token_pair(user)

        response = ok_response(
            {
                "detail": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.email,
                },
            }
        )

        set_auth_cookies(response, token_pair)
        return response


class TokenRefreshView(APIView):
    """Create a new access token from the refresh cookie."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return self.get_missing_token_response()

        try:
            access_token = create_access_token(refresh_token)
        except TokenError:
            return self.get_invalid_token_response()

        response = ok_response(
            {
                "detail": "Token refreshed",
                "access": access_token,
            }
        )
        set_access_cookie(response, access_token)

        return response

    def get_missing_token_response(self):
        return Response(
            {"detail": "Refresh token missing."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_invalid_token_response(self):
        return Response(
            {"detail": "Invalid refresh token."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    """Blacklist refresh token and clear auth cookies."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return self.get_missing_token_response()

        try:
            blacklist_refresh_token(refresh_token)
        except TokenError:
            return self.get_invalid_token_response()

        response = ok_response(
            {
                "detail": (
                    "Logout successful! All tokens will be deleted. "
                    "Refresh token is now invalid."
                ),
            }
        )
        delete_auth_cookies(response)

        return response

    def get_missing_token_response(self):
        return Response(
            {"detail": "Refresh token missing."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_invalid_token_response(self):
        return Response(
            {"detail": "Invalid refresh token."},
            status=status.HTTP_400_BAD_REQUEST,
        )