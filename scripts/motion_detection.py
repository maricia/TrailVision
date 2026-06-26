import os
os.environ["OPENCV_FFMPEG_READ_ATTEMPTS"] = "16384"

import cv2
import pandas as pd
from pathlib import Path

VIDEO_FOLDER = Path(r"I:\MTB_Video_Analytics\videos")
OUTPUT_FOLDER = Path(r"I:\MTB_Video_Analytics\output")
FRAMES_FOLDER = Path(r"I:\MTB_Video_Analytics\frames")

OUTPUT_FOLDER.mkdir(exist_ok=True)
FRAMES_FOLDER.mkdir(exist_ok=True)

video_files = list(VIDEO_FOLDER.glob("*.MP4")) + list(VIDEO_FOLDER.glob("*.mp4"))

if not video_files:
    raise FileNotFoundError("No MP4 files found in videos folder.")

video_path = video_files[0]
print(f"Scanning: {video_path.name}")

cap = cv2.VideoCapture(str(video_path))

if not cap.isOpened():
    raise RuntimeError("OpenCV could not open this video.")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

print(f"FPS: {fps}")
print(f"Frame count: {frame_count}")

scores = []
previous_gray = None
frame_number = 0

sample_every_seconds = 1
sample_every_frames = max(1, int(fps * sample_every_seconds))

while True:
    success, frame = cap.read()

    if not success:
        break

    if frame_number % sample_every_frames == 0:
        small = cv2.resize(frame, (320, 180))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if previous_gray is not None:
            diff = cv2.absdiff(previous_gray, gray)
            motion_score = diff.mean()
            seconds = frame_number / fps

            scores.append({
                "video": video_path.name,
                "timestamp_seconds": round(seconds, 2),
                "timestamp": f"{int(seconds // 60):02d}:{int(seconds % 60):02d}",
                "motion_score": round(motion_score, 2)
            })

        previous_gray = gray

    frame_number += 1

cap.release()

if not scores:
    print("No usable motion scores were created.")
    print("Next step: convert the GoPro video to a simpler MP4 using HandBrake or ffmpeg.")
    raise SystemExit

df = pd.DataFrame(scores).sort_values("motion_score", ascending=False)

csv_path = OUTPUT_FOLDER / "highlight_scores.csv"
df.to_csv(csv_path, index=False)

top = df.head(10)
print("\nTop highlight timestamps:")
print(top[["timestamp", "motion_score"]])

cap = cv2.VideoCapture(str(video_path))

for _, row in top.iterrows():
    timestamp_seconds = row["timestamp_seconds"]
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp_seconds * 1000)
    success, frame = cap.read()

    if success:
        safe_time = row["timestamp"].replace(":", "_")
        frame_path = FRAMES_FOLDER / f"{video_path.stem}_{safe_time}_score_{row['motion_score']}.jpg"
        cv2.imwrite(str(frame_path), frame)

cap.release()

print(f"\nSaved CSV: {csv_path}")
print(f"Saved frames to: {FRAMES_FOLDER}")