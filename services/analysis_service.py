from pathlib import Path
import cv2
import numpy as np
import pandas as pd

from config import OUTPUT_DIR, FRAME_DIR
from models.video import Video
from services.video_service import VideoService


class AnalysisService:
    def __init__(self):
        OUTPUT_DIR.mkdir(exist_ok=True)
        FRAME_DIR.mkdir(exist_ok=True)
        self.video_service = VideoService()

    def analyze_optical_flow(self, video: Video, sample_every_seconds: int = 1) -> list[dict]:
        video = self.video_service.ensure_converted(video)
        video_path = video.converted_path or video.original_path

        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise RuntimeError(f"Could not open video for analysis: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        sample_every_frames = max(1, int(fps * sample_every_seconds))

        previous_gray = None
        rows = []
        frame_number = 0

        while True:
            success, frame = cap.read()

            if not success:
                break

            if frame_number % sample_every_frames == 0:
                small = cv2.resize(frame, (320, 180))
                gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

                if previous_gray is not None:
                    flow = cv2.calcOpticalFlowFarneback(
                        previous_gray,
                        gray,
                        None,
                        0.5,
                        3,
                        15,
                        3,
                        5,
                        1.2,
                        0
                    )

                    dx = flow[..., 0]
                    dy = flow[..., 1]
                    magnitude, _ = cv2.cartToPolar(dx, dy)

                    avg_motion = float(np.mean(magnitude))
                    max_motion = float(np.max(magnitude))
                    horizontal_motion = float(np.mean(dx))
                    vertical_motion = float(np.mean(dy))

                    seconds = frame_number / fps

                    turn_direction = self._classify_turn(horizontal_motion)
                    terrain = self._classify_terrain(avg_motion)
                    highlight_score = self._calculate_highlight_score(
                        avg_motion,
                        max_motion,
                        horizontal_motion,
                        vertical_motion
                    )

                    rows.append({
                        "video": video_path.name,
                        "timestamp_seconds": round(seconds, 2),
                        "timestamp": f"{int(seconds // 60):02d}:{int(seconds % 60):02d}",
                        "avg_motion": round(avg_motion, 3),
                        "max_motion": round(max_motion, 3),
                        "horizontal_motion": round(horizontal_motion, 3),
                        "vertical_motion": round(vertical_motion, 3),
                        "terrain": terrain,
                        "turn_direction": turn_direction,
                        "highlight_score": round(highlight_score, 3)
                    })

                previous_gray = gray

            frame_number += 1

        cap.release()

        csv_path = OUTPUT_DIR / "analysis_metrics.csv"
        pd.DataFrame(rows).to_csv(csv_path, index=False)

        return rows

    def extract_highlight_frames(self, video: Video, metrics: list[dict], top_n: int = 10) -> list[dict]:
        video = self.video_service.ensure_converted(video)
        video_path = video.converted_path or video.original_path

        if not metrics:
            return []

        top_metrics = sorted(
            metrics,
            key=lambda row: row["highlight_score"],
            reverse=True
        )[:top_n]

        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise RuntimeError(f"Could not open video for frame extraction: {video_path}")

        extracted = []

        for row in top_metrics:
            timestamp_seconds = row["timestamp_seconds"]

            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp_seconds * 1000)
            success, frame = cap.read()

            if success:
                safe_time = row["timestamp"].replace(":", "_")
                frame_path = FRAME_DIR / f"{video_path.stem}_{safe_time}_score_{row['highlight_score']}.jpg"

                cv2.imwrite(str(frame_path), frame)

                extracted.append({
                    "video": video_path.name,
                    "timestamp_seconds": timestamp_seconds,
                    "frame_path": str(frame_path),
                    "reason": "top_highlight_score",
                    "score": row["highlight_score"]
                })

        cap.release()

        return extracted

    def _classify_turn(self, horizontal_motion: float) -> str:
        if horizontal_motion > 0.35:
            return "right"
        if horizontal_motion < -0.35:
            return "left"
        return "straight"

    def _classify_terrain(self, avg_motion: float) -> str:
        if avg_motion > 5:
            return "very rough"
        if avg_motion > 2.5:
            return "rough"
        return "smooth"

    def _calculate_highlight_score(
        self,
        avg_motion: float,
        max_motion: float,
        horizontal_motion: float,
        vertical_motion: float
    ) -> float:
        return (
            avg_motion * 10
            + max_motion
            + abs(horizontal_motion) * 5
            + abs(vertical_motion) * 5
        )