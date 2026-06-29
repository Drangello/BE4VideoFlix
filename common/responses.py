from rest_framework import status
from rest_framework.response import Response


GENERAL_AUTH_ERROR = (
    "Bitte überprüfe deine Eingaben und versuche es erneut."
)


def created_response(data):
    """Return a 201 created response."""
    return Response(data, status=status.HTTP_201_CREATED)


def ok_response(data):
    """Return a 200 OK response."""
    return Response(data, status=status.HTTP_200_OK)


def bad_request_response(message):
    """Return a 400 bad request response."""
    return Response(
        {"detail": message},
        status=status.HTTP_400_BAD_REQUEST,
    )