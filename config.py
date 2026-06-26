from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RAW_VIDEO_DIR = BASE_DIR / "raw_videos"
CONVERTED_VIDEO_DIR = BASE_DIR / "converted"

OUTPUT_DIR = BASE_DIR / "output"
FRAME_DIR = BASE_DIR / "frames"

DATABASE_PATH = BASE_DIR / "database" / "trailvision.duckdb"

DOCUMENTATION_DIR = BASE_DIR / "docs"