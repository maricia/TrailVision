from pathlib import Path
import duckdb

BASE_DIR = Path(r"I:\MTB_Video_Analytics")
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "trailvision.duckdb"

DATABASE_DIR.mkdir(exist_ok=True)

con = duckdb.connect(str(DATABASE_PATH))

con.execute("""
CREATE SEQUENCE IF NOT EXISTS seq_ride_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_video_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_conversion_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_metric_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_event_id START 1;
CREATE SEQUENCE IF NOT EXISTS seq_frame_id START 1;
""")

con.execute("""
CREATE TABLE IF NOT EXISTS rides (
    ride_id INTEGER PRIMARY KEY DEFAULT nextval('seq_ride_id'),
    ride_name TEXT,
    ride_date DATE,
    location TEXT,
    trail_name TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS videos (
    video_id INTEGER PRIMARY KEY DEFAULT nextval('seq_video_id'),
    ride_id INTEGER,
    original_filename TEXT,
    original_path TEXT,
    duration_seconds DOUBLE,
    fps DOUBLE,
    frame_count INTEGER,
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS video_conversions (
    conversion_id INTEGER PRIMARY KEY DEFAULT nextval('seq_conversion_id'),
    video_id INTEGER,
    converted_filename TEXT,
    converted_path TEXT,
    codec TEXT,
    conversion_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS frame_metrics (
    metric_id INTEGER PRIMARY KEY DEFAULT nextval('seq_metric_id'),
    video_id INTEGER,
    timestamp_seconds DOUBLE,
    timestamp_label TEXT,
    avg_motion DOUBLE,
    max_motion DOUBLE,
    horizontal_motion DOUBLE,
    vertical_motion DOUBLE,
    terrain_label TEXT,
    turn_direction TEXT,
    highlight_score DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS highlight_events (
    event_id INTEGER PRIMARY KEY DEFAULT nextval('seq_event_id'),
    video_id INTEGER,
    start_seconds DOUBLE,
    end_seconds DOUBLE,
    event_type TEXT,
    confidence DOUBLE,
    highlight_score DOUBLE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

con.execute("""
CREATE TABLE IF NOT EXISTS extracted_frames (
    frame_id INTEGER PRIMARY KEY DEFAULT nextval('seq_frame_id'),
    video_id INTEGER,
    timestamp_seconds DOUBLE,
    frame_path TEXT,
    reason TEXT,
    score DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

tables = con.execute("SHOW TABLES").fetchall()

print(f"TrailVision database created at: {DATABASE_PATH}")
print("Tables:")
for table in tables:
    print(f" - {table[0]}")

con.close()