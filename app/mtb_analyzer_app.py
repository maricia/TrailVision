import cv2
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

BASE = Path(r"I:\MTB_Video_Analytics")
OUTPUT = BASE / "output"
FRAMES = BASE / "frames"

OUTPUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)


def analyze_video(video_path):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError("Could not open video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    sample_every_frames = max(1, int(fps))

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
                    previous_gray, gray, None,
                    0.5, 3, 15, 3, 5, 1.2, 0
                )

                dx = flow[..., 0]
                dy = flow[..., 1]
                magnitude, _ = cv2.cartToPolar(dx, dy)

                seconds = frame_number / fps
                avg_motion = float(np.mean(magnitude))
                max_motion = float(np.max(magnitude))
                horizontal_motion = float(np.mean(dx))
                vertical_motion = float(np.mean(dy))

                highlight_score = avg_motion * 10 + max_motion

                rows.append({
                    "video": video_path.name,
                    "timestamp_seconds": round(seconds, 2),
                    "timestamp": f"{int(seconds // 60):02d}:{int(seconds % 60):02d}",
                    "avg_motion": round(avg_motion, 3),
                    "max_motion": round(max_motion, 3),
                    "horizontal_motion": round(horizontal_motion, 3),
                    "vertical_motion": round(vertical_motion, 3),
                    "highlight_score": round(highlight_score, 3)
                })

            previous_gray = gray

        frame_number += 1

    cap.release()

    df = pd.DataFrame(rows)

    csv_path = OUTPUT / "ride_analysis.csv"
    df.to_csv(csv_path, index=False)

    top = df.sort_values("highlight_score", ascending=False).head(10)

    cap = cv2.VideoCapture(str(video_path))

    for _, row in top.iterrows():
        cap.set(cv2.CAP_PROP_POS_MSEC, row["timestamp_seconds"] * 1000)
        success, frame = cap.read()

        if success:
            safe_time = row["timestamp"].replace(":", "_")
            frame_path = FRAMES / f"{video_path.stem}_{safe_time}_score_{row['highlight_score']}.jpg"
            cv2.imwrite(str(frame_path), frame)

    cap.release()

    return csv_path, len(top)


def select_video():
    video_file = filedialog.askopenfilename(
        title="Select MTB video",
        filetypes=[("MP4 files", "*.mp4 *.MP4")]
    )

    if not video_file:
        return

    selected_video.set(video_file)


def run_analysis():
    if not selected_video.get():
        messagebox.showwarning("No video", "Select a video first.")
        return

    try:
        status.set("Analyzing ride... dirt goblins are counting pixels.")
        root.update_idletasks()

        csv_path, frame_count = analyze_video(Path(selected_video.get()))

        status.set("Done.")
        messagebox.showinfo(
            "Analysis Complete",
            f"Saved CSV:\n{csv_path}\n\nSaved {frame_count} highlight frames."
        )

    except Exception as e:
        status.set("Error.")
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("MTB Video Analyzer")
root.geometry("650x260")

selected_video = tk.StringVar()
status = tk.StringVar(value="Select a GoPro video to begin.")

tk.Label(root, text="MTB Video Analyzer", font=("Arial", 18, "bold")).pack(pady=15)

tk.Button(root, text="Select Video", command=select_video, width=25).pack()

tk.Label(root, textvariable=selected_video, wraplength=600).pack(pady=10)

tk.Button(root, text="Analyze Ride", command=run_analysis, width=25).pack(pady=10)

tk.Label(root, textvariable=status).pack(pady=15)

root.mainloop()