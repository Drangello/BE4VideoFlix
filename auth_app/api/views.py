from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import RegisterSerializer


class RegisterView(APIView):
    """Handle user registration."""

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "token": "",
            },
            status=status.HTTP_201_CREATED,
        )
