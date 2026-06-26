import cv2
import pandas as pd
import numpy as np
from pathlib import Path

VIDEO_PATH = Path(r"I:\MTB_Video_Analytics\videos\GH010226.mp4")
OUTPUT_FOLDER = Path(r"I:\MTB_Video_Analytics\output")
OUTPUT_FOLDER.mkdir(exist_ok=True)

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

print(f"Video: {VIDEO_PATH.name}")
print(f"FPS: {fps:.2f}")
print(f"Frames: {frame_count}")
print(f"Duration: {duration:.2f} seconds")

sample_every_seconds = 1
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
                pyr_scale=0.5,
                levels=3,
                winsize=15,
                iterations=3,
                poly_n=5,
                poly_sigma=1.2,
                flags=0
            )

            dx = flow[..., 0]
            dy = flow[..., 1]

            magnitude, angle = cv2.cartToPolar(dx, dy)

            avg_motion = float(np.mean(magnitude))
            max_motion = float(np.max(magnitude))
            horizontal_motion = float(np.mean(dx))
            vertical_motion = float(np.mean(dy))

            seconds = frame_number / fps

            turn_direction = "straight"
            if horizontal_motion > 0.35:
                turn_direction = "right"
            elif horizontal_motion < -0.35:
                turn_direction = "left"

            terrain = "smooth"
            if avg_motion > 2.5:
                terrain = "rough"
            if avg_motion > 5:
                terrain = "very rough"

            rows.append({
                "video": VIDEO_PATH.name,
                "timestamp_seconds": round(seconds, 2),
                "timestamp": f"{int(seconds // 60):02d}:{int(seconds % 60):02d}",
                "avg_motion": round(avg_motion, 3),
                "max_motion": round(max_motion, 3),
                "horizontal_motion": round(horizontal_motion, 3),
                "vertical_motion": round(vertical_motion, 3),
                "turn_direction": turn_direction,
                "terrain": terrain
            })

        previous_gray = gray

    frame_number += 1

cap.release()

df = pd.DataFrame(rows)

csv_path = OUTPUT_FOLDER / "optical_flow_metrics.csv"
df.to_csv(csv_path, index=False)

print("\nTop motion sections:")
print(df.sort_values("avg_motion", ascending=False).head(15))

print(f"\nSaved: {csv_path}")