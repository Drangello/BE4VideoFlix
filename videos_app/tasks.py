from videos_app.models import Video
from videos_app.services.ffmpeg_service import process_video


def process_video_task(video_id):
    """Process a video in the background."""
    video = Video.objects.filter(pk=video_id).first()

    if not video:
        return

    process_video(video)