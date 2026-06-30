import sys
import cv2
import pandas as pd
import numpy as np
import customtkinter as ctk
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

def format_duration(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def get_video_metadata(video_path):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps else 0

    cap.release()

    size_gb = Path(video_path).stat().st_size / (1024 ** 3)

    return {
        "name": Path(video_path).name,
        "path": str(video_path),
        "duration": format_duration(duration),
        "fps": round(fps, 1),
        "frames": int(frame_count),
        "resolution": f"{width} x {height}",
        "size": f"{size_gb:.2f} GB",
    }

def select_video():
    video_file = filedialog.askopenfilename(
        title="Select MTB video",
        filetypes=[("MP4 files", "*.mp4 *.MP4")]
    )

    if not video_file:
        return

    selected_video.set(video_file)

    metadata = get_video_metadata(video_file)

    if metadata:
        video_name_var.set(metadata["name"])
        video_details_var.set(
            f"Duration: {metadata['duration']}\n"
            f"Resolution: {metadata['resolution']}\n"
            f"FPS: {metadata['fps']}\n"
            f"Frames: {metadata['frames']:,}\n"
            f"Size: {metadata['size']}"
        )

    status.set("Video loaded. Ready to analyze.")


def run_analysis():
    if not selected_video.get():
        messagebox.showwarning("No video", "Select a video first.")
        return

    status.set("Preparing analysis...")
    root.update_idletasks()
    progress_bar.set(0)

    def on_progress(processed, total):
        percent = int((processed / total) * 100) if total else 0
        progress_bar.config(mode='determinate')
        #progress_bar.set(percent / 100)
        progress_bar.set(percent / 100)
        progress_text.configure(text=f"Progress: {percent}%")
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
        progress_bar.set(1.0)
        progress_text.configure(text="Progress: 100%")
        #progress_bar.set(percent / 100)
        highlight_count_var.set(str(frame_count))
        motion_score_var.set("82")
        flow_score_var.set("91")
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
            video = video_service.prepare_video(Path(selected_video.get()))
            progress_bar.config(mode='determinate')
            progress_bar.set(0)
            status.set("Analyzing video...")

            metrics = analysis_service.analyze_optical_flow(
                video, progress_callback=lambda p, t: root.after(0, on_progress, p, t)
            )

            status.set("Extracting highlight frames...")
            frames = analysis_service.extract_highlight_frames(video, metrics, top_n=10)
            progress_bar.config(mode='determinate')

            csv_path = OUTPUT / "ride_analysis.csv"
            root.after(0, on_done, csv_path, len(frames))

        except Exception as e:
            tb = traceback.format_exc()
            root.after(0, on_error, e, tb)

    threading.Thread(target=worker, daemon=True).start()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("TrailVision v1.0")
root.geometry("950x600")
root.minsize(900, 550)

selected_video = tk.StringVar()
status = tk.StringVar(value="Ready. Select a GoPro video to begin.")

step_video_var = tk.StringVar(value="○ Video Loaded")
step_frames_var = tk.StringVar(value="○ Reading Frames")
step_flow_var = tk.StringVar(value="○ Optical Flow Analysis")
step_highlights_var = tk.StringVar(value="○ Highlight Detection")
step_export_var = tk.StringVar(value="○ Exporting Results")

highlight_count_var = tk.StringVar(value="0")
motion_score_var = tk.StringVar(value="Waiting")
flow_score_var = tk.StringVar(value="Waiting")

# Main layout
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Sidebar
sidebar = ctk.CTkFrame(root, width=220, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_rowconfigure(8, weight=1)

logo = ctk.CTkLabel(
    sidebar,
    text="🚵\nTrailVision",
    font=ctk.CTkFont(size=28, weight="bold"),
    justify="center"
)
logo.grid(row=0, column=0, padx=20, pady=(30, 10))

subtitle = ctk.CTkLabel(
    sidebar,
    text="AI Powered MTB\nVideo Analytics",
    font=ctk.CTkFont(size=14),
    text_color="gray70",
    justify="center"
)
subtitle.grid(row=1, column=0, padx=20, pady=(0, 30))

ctk.CTkButton(sidebar, text="Analyze", height=44).grid(row=2, column=0, padx=20, pady=8, sticky="ew")
ctk.CTkButton(sidebar, text="Results", height=44, fg_color="transparent").grid(row=3, column=0, padx=20, pady=8, sticky="ew")
ctk.CTkButton(sidebar, text="Highlights", height=44, fg_color="transparent").grid(row=4, column=0, padx=20, pady=8, sticky="ew")
ctk.CTkButton(sidebar, text="Settings", height=44, fg_color="transparent").grid(row=5, column=0, padx=20, pady=8, sticky="ew")

ready_box = ctk.CTkFrame(sidebar)
ready_box.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

ctk.CTkLabel(ready_box, text="● Ready", text_color="#66ff66").pack(anchor="w", padx=15, pady=(12, 2))
ctk.CTkLabel(ready_box, text="TrailVision v1.0.0", text_color="gray70").pack(anchor="w", padx=15, pady=(0, 12))

# Main content
main = ctk.CTkFrame(root, corner_radius=0, fg_color="#111111")
main.grid(row=0, column=1, sticky="nsew")
main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=1)

title = ctk.CTkLabel(
    main,
    text="TrailVision v1.0.0  |  Computer Vision MTB Analyzer",
    font=ctk.CTkFont(size=18, weight="bold")
)
title.grid(row=0, column=0, columnspan=2, padx=25, pady=(25, 15), sticky="w")

# Video card
video_card = ctk.CTkFrame(main, corner_radius=14)
video_card.grid(row=1, column=0, padx=25, pady=10, sticky="nsew")
video_name_var = tk.StringVar(value="No video selected")
video_details_var = tk.StringVar(value="Select a GoPro video to begin.")

video_name_label = ctk.CTkLabel(
    video_card,
    textvariable=video_name_var,
    font=ctk.CTkFont(size=20, weight="bold"),
    anchor="w"
)
video_name_label.pack(fill="x", padx=20, pady=(10, 2))

video_details_label = ctk.CTkLabel(
    video_card,
    textvariable=video_details_var,
    text_color="gray75",
    justify="left",
    anchor="w",
    wraplength=420
)
video_details_label.pack(fill="x", padx=20, pady=(0, 15))

ctk.CTkLabel(
    video_card,
    text="📹  1. Select GoPro Video",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(anchor="w", padx=20, pady=(20, 10))

selected_label = ctk.CTkLabel(
    video_card,
    textvariable=selected_video,
    wraplength=420,
    text_color="gray75"
)
selected_label.pack(anchor="w", padx=20, pady=(5, 15))

select_btn = ctk.CTkButton(
    video_card,
    text="📂 Select GoPro Video",
    command=select_video,
    height=50,
    font=ctk.CTkFont(size=16, weight="bold")
)
select_btn.pack(fill="x", padx=20, pady=(10, 20))

# Analyze card
analyze_card = ctk.CTkFrame(main, corner_radius=14)
analyze_card.grid(row=2, column=0, padx=25, pady=10, sticky="nsew")



ctk.CTkLabel(
    analyze_card,
    text="🧠  2. Analyze Ride",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(anchor="w", padx=20, pady=(20, 10))

analyze_btn = ctk.CTkButton(
    analyze_card,
    text="▶ Analyze Ride",
    command=run_analysis,
    height=70,
    font=ctk.CTkFont(size=22, weight="bold")
)
analyze_btn.pack(fill="x", padx=20, pady=(15, 10))

ctk.CTkLabel(
    analyze_card,
    text="💡Tip: Best results come from clear GoPro footage with strong motion and trail texture.",
    text_color="gray75",
    justify="left",
    wraplength=390
).pack(anchor="w", padx=20, pady=(5, 20))

# Status card
status_card = ctk.CTkFrame(main, corner_radius=14)
status_card.grid(row=1, column=1, rowspan=2, padx=(0, 25), pady=10, sticky="nsew")

for step_var in [
    step_video_var,
    step_frames_var,
    step_flow_var,
    step_highlights_var,
    step_export_var
]:
    ctk.CTkLabel(
        status_card,
        textvariable=step_var,
        anchor="w",
        font=ctk.CTkFont(size=14)
    ).pack(fill="x", padx=20, pady=4)

ctk.CTkLabel(
    status_card,
    text="⚡ Analysis Status",
    font=ctk.CTkFont(size=20, weight="bold"),
    anchor="w"
).pack(fill="x", padx=20, pady=(20, 12))

status_label = ctk.CTkLabel(
    status_card,
    textvariable=status,
    font=ctk.CTkFont(size=15),
    text_color="gray85",
    wraplength=350
)
status_label.pack(anchor="w", padx=20, pady=(0, 20))

progress_bar = ctk.CTkProgressBar(status_card, height=16)
progress_bar.pack(fill="x", padx=20, pady=(10, 10))
progress_bar.set(0)

progress_text = ctk.CTkLabel(status_card, text="Progress: 0%", text_color="gray75")
progress_text.pack(anchor="w", padx=20, pady=(0, 20))

ctk.CTkLabel(
    status_card,
    text="🏆 Results Summary",
    font=ctk.CTkFont(size=18, weight="bold"),
    anchor="w"
).pack(fill="x", padx=20, pady=(25, 10))

summary_box = ctk.CTkFrame(status_card)
summary_box.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(summary_box, text="Highlights Found", text_color="gray70").pack(anchor="w", padx=15, pady=(12, 0))
ctk.CTkLabel(summary_box, text="Waiting for analysis", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(0, 12))
ctk.CTkLabel(summary_box, text="Highlights Found").pack()
ctk.CTkLabel(
    summary_box,
    textvariable=highlight_count_var,
    font=ctk.CTkFont(size=24, weight="bold")
).pack()

ctk.CTkLabel(summary_box, text="Motion Score").pack()
ctk.CTkLabel(
    summary_box,
    textvariable=motion_score_var,
    font=ctk.CTkFont(size=24, weight="bold")
).pack()

ctk.CTkLabel(summary_box, text="Flow Score").pack()
ctk.CTkLabel(
    summary_box,
    textvariable=flow_score_var,
    font=ctk.CTkFont(size=24, weight="bold")
).pack()

root.mainloop()