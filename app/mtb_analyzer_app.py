import sys
import cv2
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Ensure repository root is on sys.path so sibling packages (services, models, etc.)
# can be imported even when running this file from the `app/` directory.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from services.video_service import VideoService
from services.analysis_service import AnalysisService
import threading
import time
import traceback
from tkinter import ttk

BASE = Path(r"I:\MTB_Video_Analytics")
OUTPUT = BASE / "output"
FRAMES = BASE / "frames"

OUTPUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

video_service = VideoService()
analysis_service = AnalysisService()

# UI state for progress/ETA
_analysis_start_time = None


def analyze_video(video_path):
    # kept for backwards compatibility but not used by the GUI threading flow
    video = video_service.prepare_video(video_path)
    metrics = analysis_service.analyze_optical_flow(video)
    frames = analysis_service.extract_highlight_frames(video, metrics, top_n=10)

    csv_path = OUTPUT / "ride_analysis.csv"
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
    # Start background analysis to keep the UI responsive and show progress/ETA
    status.set("Analyzing ride...")
    root.update_idletasks()

    progress_bar['value'] = 0

    def on_progress(processed, total):
        percent = int((processed / total) * 100) if total else 0
        progress_bar.config(mode='determinate')
        progress_bar['value'] = min(100, percent)
        elapsed = time.time() - _analysis_start_time if _analysis_start_time else 0
        rate = (processed / elapsed) if elapsed > 0 else 0
        if rate > 0 and total:
            remaining = max(0, (total - processed) / rate)
            eta = time.strftime('%M:%S', time.gmtime(remaining))
        else:
            eta = 'calculating'

        status.set(f"Analyzing... {percent}% | ETA {eta}")

    def on_done(csv_path, frame_count):
        status.set("Done.")
        progress_bar['value'] = 100
        messagebox.showinfo(
            "Analysis Complete",
            f"Saved CSV:\n{csv_path}\n\nSaved {frame_count} highlight frames."
        )

    def on_error(e, tb):
        status.set("Error.")
        print(tb)
        messagebox.showerror("Error", f"{e}\n\nSee console for full traceback:\n\n{tb}")

    def worker():
        global _analysis_start_time
        try:
            _analysis_start_time = time.time()
            status.set("Converting video...")
            progress_bar.config(mode='indeterminate')
            progress_bar.start(10)
            video = video_service.prepare_video(Path(selected_video.get()))

            progress_bar.stop()
            progress_bar.config(mode='determinate')
            progress_bar['value'] = 0

            # analysis_service will call our callback periodically
            metrics = analysis_service.analyze_optical_flow(
                video, progress_callback=lambda p, t: root.after(0, on_progress, p, t)
            )

            frames = analysis_service.extract_highlight_frames(video, metrics, top_n=10)

            csv_path = OUTPUT / "ride_analysis.csv"
            root.after(0, on_done, csv_path, len(frames))

        except Exception as e:
            tb = traceback.format_exc()
            root.after(0, on_error, e, tb)

    threading.Thread(target=worker, daemon=True).start()


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

progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate')
progress_bar.pack(pady=5)

root.mainloop()