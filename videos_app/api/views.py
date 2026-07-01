from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from videos_app.api.serializers import VideoListSerializer
from videos_app.models import Video


class VideoListView(ListAPIView):
    """Return all processed videos for authenticated users."""

    serializer_class = VideoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return processed videos ordered by newest first."""
        return Video.objects.filter(is_processed=True)
