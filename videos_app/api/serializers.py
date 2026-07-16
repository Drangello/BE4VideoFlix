from rest_framework import serializers

from videos_app.models import Video


class VideoListSerializer(serializers.ModelSerializer):
    """Serialize processed videos for the dashboard."""

    thumbnail_url = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            "id",
            "created_at",
            "title",
            "description",
            "thumbnail_url",
            "thumbnail",
            "category",
        )

    def get_thumbnail_url(self, video):
        """Return the absolute thumbnail URL."""
        return self.build_thumbnail_url(video)

    def get_thumbnail(self, video):
        """Return the thumbnail URL for frontend compatibility."""
        return self.build_thumbnail_url(video)

    def build_thumbnail_url(self, video):
        """Build an absolute thumbnail URL."""
        if not video.thumbnail:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(video.thumbnail.url)

        return video.thumbnail.url