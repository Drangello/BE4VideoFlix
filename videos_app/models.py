from django.db import models


class Video(models.Model):
    """Store a source video and its streaming metadata."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    source_file = models.FileField(upload_to="videos/source/")
    thumbnail = models.FileField(
        upload_to="videos/thumbnails/",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
