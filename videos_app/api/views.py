from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from videos_app.api.serializers import VideoListSerializer
from videos_app.models import Video
from videos_app.services.streaming_service import (
    get_hls_file_path,
    get_hls_file_response,
)


class VideoListView(ListAPIView):
    """Return all processed videos for authenticated users."""

    serializer_class = VideoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return processed videos ordered by newest first."""
        return Video.objects.filter(is_processed=True)


class HLSPlaylistView(APIView):
    """Return an HLS playlist file."""

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        file_path = get_hls_file_path(
            movie_id,
            resolution,
            "index.m3u8",
        )

        return get_hls_file_response(
            file_path,
            "application/vnd.apple.mpegurl",
        )


class HLSSegmentView(APIView):
    """Return an HLS video segment."""

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        file_path = get_hls_file_path(
            movie_id,
            resolution,
            segment,
        )

        return get_hls_file_response(
            file_path,
            "video/MP2T",
        )