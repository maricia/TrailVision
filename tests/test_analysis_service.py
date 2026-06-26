import sys
from pathlib import Path

BASE_DIR = Path(r"I:\MTB_Video_Analytics")
sys.path.append(str(BASE_DIR))

from services.video_service import VideoService
from services.analysis_service import AnalysisService

video_path = BASE_DIR / "raw_videos" / "GH010226.MP4"

video_service = VideoService()
analysis_service = AnalysisService()

video = video_service.prepare_video(video_path)

metrics = analysis_service.analyze_optical_flow(video)
frames = analysis_service.extract_highlight_frames(video, metrics, top_n=10)

print(video.summary())
print()
print(f"Metrics created: {len(metrics)}")
print(f"Frames extracted: {len(frames)}")

print("\nTop 5 highlights:")
for row in sorted(metrics, key=lambda x: x["highlight_score"], reverse=True)[:5]:
    print(row["timestamp"], row["highlight_score"], row["terrain"], row["turn_direction"])