from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List

from models.video import Video


@dataclass
class Ride:
    ride_name: str
    ride_date: Optional[date] = None
    location: Optional[str] = None
    trail_name: Optional[str] = None
    notes: Optional[str] = None
    ride_id: Optional[int] = None
    videos: List[Video] = field(default_factory=list)

    def add_video(self, video: Video) -> None:
        self.videos.append(video)

    def video_count(self) -> int:
        return len(self.videos)

    def summary(self) -> str:
        return (
            f"Ride: {self.ride_name}\n"
            f"Date: {self.ride_date}\n"
            f"Location: {self.location}\n"
            f"Trail: {self.trail_name}\n"
            f"Videos: {self.video_count()}"
        )