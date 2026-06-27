import subprocess
from pathlib import Path
import cv2

from config import CONVERTED_VIDEO_DIR
from models.video import Video


class VideoService:
    def __init__(self):
        CONVERTED_VIDEO_DIR.mkdir(exist_ok=True)

    def read_metadata(self, video: Video) -> Video:
        cap = cv2.VideoCapture(str(video.original_path))

        if not cap.isOpened():
            raise RuntimeError(f"Could not open video: {video.original_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        duration_seconds = frame_count / fps if fps else None

        cap.release()

        video.fps = fps
        video.frame_count = frame_count
        video.width = width
        video.height = height
        video.duration_seconds = duration_seconds

        return video

    def get_converted_path(self, video: Video) -> Path:
        return CONVERTED_VIDEO_DIR / f"{video.original_path.stem}_converted.mp4"

    def convert_to_mp4(self, video: Video, overwrite: bool = False) -> Video:
        converted_path = self.get_converted_path(video)

        if converted_path.exists() and not overwrite:
            video.converted_path = converted_path
            return video

        command = [
            "ffmpeg",
            "-y" if overwrite else "-n",
            "-i", str(video.original_path),
            "-map", "0:v:0",
            "-an",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            str(converted_path)
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg conversion failed.\n\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )

        video.converted_path = converted_path
        return video

    def ensure_converted(self, video: Video, overwrite: bool = False) -> Video:
        converted_path = self.get_converted_path(video)

        if video.converted_path is not None and video.converted_path.exists():
            return video

        if converted_path.exists() and not overwrite:
            video.converted_path = converted_path
            return video

        if not video.original_path.exists():
            raise FileNotFoundError(f"Original video file does not exist: {video.original_path}")

        if video.duration_seconds is None or video.fps is None or video.frame_count is None:
            video = self.read_metadata(video)

        return self.convert_to_mp4(video, overwrite=overwrite)

    def prepare_video(self, video_path: Path, overwrite: bool = False) -> Video:
        video = Video(original_path=video_path)

        video = self.read_metadata(video)
        video = self.convert_to_mp4(video, overwrite=overwrite)

        return video