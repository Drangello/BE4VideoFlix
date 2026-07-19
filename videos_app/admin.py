import django_rq
from django.contrib import admin
from django.db import transaction

from videos_app.models import Video
from videos_app.tasks import process_video_task


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Configure videos in the Django admin."""

    fields = (
        "title",
        "description",
        "category",
        "source_file",
    )
    list_display = (
        "title",
        "category",
        "is_processed",
        "created_at",
    )
    list_filter = ("category", "is_processed")
    search_fields = ("title", "description")

    def save_model(self, request, video, form, change):
        """Save a video and queue processing when needed."""
        should_process = self.should_process_video(form, change)

        if should_process:
            video.is_processed = False
            video.thumbnail = ""

        super().save_model(request, video, form, change)

        if should_process:
            self.enqueue_video_processing(video.id)

    def should_process_video(self, form, change):
        """Return whether the video file should be processed."""
        return not change or "source_file" in form.changed_data

    def enqueue_video_processing(self, video_id):
        """Queue video processing after database commit."""
        transaction.on_commit(
            lambda: django_rq.enqueue(process_video_task, video_id)
        )