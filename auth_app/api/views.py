from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from auth_app.api.serializers import (
    LoginSerializer,
    PasswordConfirmSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
)
from auth_app.services.account_service import (
    activate_account,
    confirm_password_reset,
    register_account,
    request_password_reset,
)
from auth_app.services.token_service import (
    blacklist_refresh_token,
    create_access_token,
    create_token_pair,
    delete_auth_cookies,
    set_access_cookie,
    set_auth_cookies,
)
from common.responses import created_response, ok_response

LOGOUT_DETAIL = (
    "Logout successful! All tokens will be deleted. "
    "Refresh token is now invalid."
)


class RegisterView(APIView):
    """Handle user registration."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, activation_data = register_account(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return created_response(
            {
                "user": {"id": user.id, "email": user.email},
                "token": activation_data["token"],
            }
        )


class ActivateView(APIView):
    """Activate a user account."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        if not activate_account(uidb64, token):
            return self.get_error_response()
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
                "user": {"id": user.id, "username": user.email},
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
        response = ok_response({"detail": "Token refreshed", "access": access_token})
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
        response = ok_response({"detail": LOGOUT_DETAIL})
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


class PasswordResetView(APIView):
    """Queue a password reset email."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_password_reset(serializer.validated_data["email"])
        return ok_response(
            {"detail": "An email has been sent to reset your password."}
        )


class PasswordConfirmView(APIView):
    """Set a new password with a valid reset token."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not confirm_password_reset(
            uidb64,
            token,
            serializer.validated_data["new_password"],
        ):
            return self.get_invalid_token_response()
        return ok_response(
            {"detail": "Your Password has been successfully reset."}
        )

    def get_invalid_token_response(self):
        return Response(
            {"detail": "Invalid or expired password reset token."},
            status=status.HTTP_400_BAD_REQUEST,
        )
