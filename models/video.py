from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Video:
    original_path: Path
    video_id: Optional[int] = None
    ride_id: Optional[int] = None
    converted_path: Optional[Path] = None
    duration_seconds: Optional[float] = None
    fps: Optional[float] = None
    frame_count: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None

    @property
    def original_filename(self) -> str:
        return self.original_path.name

    @property
    def converted_filename(self) -> Optional[str]:
        if self.converted_path is None:
            return None
        return self.converted_path.name

    def has_conversion(self) -> bool:
        return self.converted_path is not None and self.converted_path.exists()

    def summary(self) -> str:
        return (
            f"Video: {self.original_filename}\n"
            f"Duration: {self.duration_seconds}\n"
            f"FPS: {self.fps}\n"
            f"Frames: {self.frame_count}\n"
            f"Size: {self.width}x{self.height}\n"
            f"Converted: {self.converted_path}"
        )