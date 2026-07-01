
import subprocess
from pathlib import Path

from django.conf import settings

RESOLUTION_HEIGHTS = {
    "480p": 480,
    "720p": 720,
    "1080p": 1080,
}


def process_video(video):
    """Create thumbnail and HLS files for a video."""
    create_thumbnail(video)

    for resolution, height in RESOLUTION_HEIGHTS.items():
        create_hls_playlist(video, resolution, height)

    mark_video_processed(video)


def create_thumbnail(video):
    """Create and save a thumbnail image."""
    output_path = get_thumbnail_path(video)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    run_ffmpeg(build_thumbnail_command(video, output_path))

    video.thumbnail.name = get_media_relative_path(output_path)
    video.save(update_fields=["thumbnail"])


def create_hls_playlist(video, resolution, height):
    """Create one HLS playlist with video segments."""
    output_dir = get_hls_output_dir(video, resolution)
    output_dir.mkdir(parents=True, exist_ok=True)

    command = build_hls_command(video, output_dir, height)
    run_ffmpeg(command)


def build_thumbnail_command(video, output_path):
    """Build the FFmpeg thumbnail command."""
    return [
        "ffmpeg",
        "-y",
        "-ss",
        "00:00:01",
        "-i",
        video.source_file.path,
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]


def build_hls_command(video, output_dir, height):
    """Build the FFmpeg HLS conversion command."""
    return [
        "ffmpeg",
        "-y",
        "-i",
        video.source_file.path,
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-vf",
        f"scale=-2:{height}",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-flags",
        "+cgop",
        "-force_key_frames",
        "expr:gte(t,n_forced*6)",
        "-f",
        "hls",
        "-hls_time",
        "6",
        "-hls_list_size",
        "0",
        "-hls_playlist_type",
        "vod",
        "-hls_segment_filename",
        str(output_dir / "segment_%03d.ts"),
        str(output_dir / "index.m3u8"),
    ]


def run_ffmpeg(command):
    """Run an FFmpeg command and raise errors."""
    subprocess.run(command, check=True)


def get_thumbnail_path(video):
    """Return the thumbnail output path."""
    return Path(settings.MEDIA_ROOT) / "videos" / "thumbnails" / (
        f"{video.pk}.jpg"
    )


def get_hls_output_dir(video, resolution):
    """Return the HLS directory for one resolution."""
    return Path(settings.MEDIA_ROOT) / "videos" / "hls" / str(
        video.pk
    ) / resolution


def get_media_relative_path(file_path):
    """Return a path relative to the media directory."""
    return file_path.relative_to(settings.MEDIA_ROOT).as_posix()


def mark_video_processed(video):
    """Mark a video as successfully processed."""
    video.is_processed = True
    video.save(update_fields=["is_processed"])