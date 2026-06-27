import cv2
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from services.video_service import VideoService
from services.analysis_service import AnalysisService

BASE = Path(r"I:\MTB_Video_Analytics")
OUTPUT = BASE / "output"
FRAMES = BASE / "frames"

OUTPUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

video_service = VideoService()
analysis_service = AnalysisService()


def analyze_video(video_path):
    video = video_service.prepare_video(video_path)
    metrics = analysis_service.analyze_optical_flow(video)
    frames = analysis_service.extract_highlight_frames(video, metrics, top_n=10)

    csv_path = OUTPUT / "ride_analysis.csv"
    # Keep the UI contract of returning CSV path and frame count.
    return csv_path, len(frames)


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
        import traceback
        tb = traceback.format_exc()
        print(tb)
        # show both the exception message and the full traceback to help debugging
        messagebox.showerror("Error", f"{e}\n\nSee console for full traceback:\n\n{tb}")


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