from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


VALID_RESOLUTIONS = ("480p", "720p", "1080p")


def get_hls_file_path(movie_id, resolution, filename):
    """Return the path to an HLS file."""
    if resolution not in VALID_RESOLUTIONS:
        raise Http404("Resolution not found.")

    return (
        Path(settings.MEDIA_ROOT)
        / "videos"
        / "hls"
        / str(movie_id)
        / resolution
        / filename
    )


def get_hls_file_response(file_path, content_type):
    """Return an HLS file response."""
    if not file_path.exists():
        raise Http404("HLS file not found.")

    return FileResponse(
        open(file_path, "rb"),
        content_type=content_type,
    )
