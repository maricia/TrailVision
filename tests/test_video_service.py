import sys
from pathlib import Path

BASE_DIR = Path(r"I:\MTB_Video_Analytics")
sys.path.append(str(BASE_DIR))

from services.video_service import VideoService

video_path = BASE_DIR / "raw_videos" / "GH010226.MP4"

service = VideoService()
video = service.prepare_video(video_path)

print(video.summary())