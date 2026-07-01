from django.contrib import admin

from videos_app.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Configure videos in the Django admin."""

    list_display = (
        "title",
        "category",
        "is_processed",
        "created_at",
    )
    list_filter = ("category", "is_processed")
    search_fields = ("title", "description")
    readonly_fields = ("created_at",)