from pathlib import Path
import duckdb


class DatabaseService:
    def __init__(self):
        base_dir = Path(r"I:\MTB_Video_Analytics")
        self.database_path = base_dir / "database" / "trailvision.duckdb"

    def connect(self):
        return duckdb.connect(str(self.database_path))

    def create_ride(self, ride_name, ride_date=None, location=None, trail_name=None, notes=None):
        with self.connect() as con:
            result = con.execute(
                """
                INSERT INTO rides (ride_name, ride_date, location, trail_name, notes)
                VALUES (?, ?, ?, ?, ?)
                RETURNING ride_id;
                """,
                [ride_name, ride_date, location, trail_name, notes]
            ).fetchone()

        return result[0]

    def add_video(self, ride_id, original_filename, original_path, duration_seconds, fps, frame_count, width, height):
        with self.connect() as con:
            result = con.execute(
                """
                INSERT INTO videos (
                    ride_id,
                    original_filename,
                    original_path,
                    duration_seconds,
                    fps,
                    frame_count,
                    width,
                    height
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                RETURNING video_id;
                """,
                [
                    ride_id,
                    original_filename,
                    original_path,
                    duration_seconds,
                    fps,
                    frame_count,
                    width,
                    height
                ]
            ).fetchone()

        return result[0]

    def add_video_conversion(self, video_id, converted_filename, converted_path, codec="libx264", conversion_status="success"):
        with self.connect() as con:
            result = con.execute(
                """
                INSERT INTO video_conversions (
                    video_id,
                    converted_filename,
                    converted_path,
                    codec,
                    conversion_status
                )
                VALUES (?, ?, ?, ?, ?)
                RETURNING conversion_id;
                """,
                [
                    video_id,
                    converted_filename,
                    converted_path,
                    codec,
                    conversion_status
                ]
            ).fetchone()

        return result[0]

    def add_frame_metrics(self, video_id, metrics):
        if not metrics:
            return 0

        rows = []
        for row in metrics:
            rows.append([
                video_id,
                row.get("timestamp_seconds"),
                row.get("timestamp"),
                row.get("avg_motion"),
                row.get("max_motion"),
                row.get("horizontal_motion"),
                row.get("vertical_motion"),
                row.get("terrain"),
                row.get("turn_direction"),
                row.get("highlight_score"),
            ])

        with self.connect() as con:
            con.executemany(
                """
                INSERT INTO frame_metrics (
                    video_id,
                    timestamp_seconds,
                    timestamp_label,
                    avg_motion,
                    max_motion,
                    horizontal_motion,
                    vertical_motion,
                    terrain_label,
                    turn_direction,
                    highlight_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                rows
            )

        return len(rows)

    def add_extracted_frame(self, video_id, timestamp_seconds, frame_path, reason, score):
        with self.connect() as con:
            result = con.execute(
                """
                INSERT INTO extracted_frames (
                    video_id,
                    timestamp_seconds,
                    frame_path,
                    reason,
                    score
                )
                VALUES (?, ?, ?, ?, ?)
                RETURNING frame_id;
                """,
                [video_id, timestamp_seconds, frame_path, reason, score]
            ).fetchone()

        return result[0]

    def list_tables(self):
        with self.connect() as con:
            return con.execute("SHOW TABLES").fetchall()