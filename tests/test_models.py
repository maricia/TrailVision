import sys
from pathlib import Path

BASE_DIR = Path(r"I:\MTB_Video_Analytics")
sys.path.append(str(BASE_DIR))

from models.ride import Ride
from models.video import Video

video = Video(
    original_path=BASE_DIR / "raw_videos" / "GH010226.MP4",
    duration_seconds=318.12,
    fps=29.97,
    frame_count=9534,
    width=2704,
    height=2028
)

ride = Ride(
    ride_name="First TrailVision Test Ride",
    location="Midland/Odessa",
    trail_name="Test Loop",
    notes="Testing Ride and Video models"
)

ride.add_video(video)

print(ride.summary())
print()
print(video.summary())