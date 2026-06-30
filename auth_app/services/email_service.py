from urllib.parse import urljoin

from django.conf import settings


def build_activation_url(uidb64, token):
    """Build the frontend activation URL."""

    activation_path = f"/activate/{uidb64}/{token}/"

    return urljoin(
        settings.FRONTEND_BASE_URL,
        activation_path,
    )
