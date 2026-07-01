import django_rq
from django.contrib import admin

from videos_app.models import Video
from videos_app.tasks import process_video_task


@admin.action(description="Ausgewählte Videos verarbeiten")
def process_selected_videos(modeladmin, request, queryset):
    """Queue selected videos for HLS processing."""
    for video in queryset:
        video.is_processed = False
        video.save(update_fields=["is_processed"])
        django_rq.enqueue(process_video_task, video.id)

    modeladmin.message_user(request, "Video-Verarbeitung wurde gestartet.")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Configure videos in the Django admin."""

    actions = [process_selected_videos]
    list_display = (
        "title",
        "category",
        "is_processed",
        "created_at",
    )
    list_filter = ("category", "is_processed")
    search_fields = ("title", "description")
    readonly_fields = ("created_at",)