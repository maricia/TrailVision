# TrailVision Data Dictionary

## Table: rides

| Column | Type | Description |
|---|---|---|
| ride_id | INTEGER | Unique ride identifier |
| ride_name | TEXT | User-friendly ride name |
| ride_date | DATE | Date of ride |
| location | TEXT | General ride location |
| trail_name | TEXT | Trail or park name |
| notes | TEXT | Optional ride notes |
| created_at | TIMESTAMP | Record creation timestamp |

## Table: videos

| Column | Type | Description |
|---|---|---|
| video_id | INTEGER | Unique video identifier |
| ride_id | INTEGER | Related ride |
| original_filename | TEXT | Original GoPro file name |
| original_path | TEXT | Full path to original file |
| duration_seconds | DOUBLE | Video duration |
| fps | DOUBLE | Frames per second |
| frame_count | INTEGER | Total frame count |
| width | INTEGER | Video width |
| height | INTEGER | Video height |
| created_at | TIMESTAMP | Record creation timestamp |

## Table: video_conversions

| Column | Type | Description |
|---|---|---|
| conversion_id | INTEGER | Unique conversion identifier |
| video_id | INTEGER | Related video |
| converted_filename | TEXT | Converted MP4 file name |
| converted_path | TEXT | Full path to converted file |
| codec | TEXT | Conversion codec |
| conversion_status | TEXT | Success, failed, skipped |
| created_at | TIMESTAMP | Record creation timestamp |

## Table: frame_metrics

| Column | Type | Description |
|---|---|---|
| metric_id | INTEGER | Unique metric identifier |
| video_id | INTEGER | Related video |
| timestamp_seconds | DOUBLE | Timestamp in seconds |
| timestamp_label | TEXT | Human-readable timestamp |
| avg_motion | DOUBLE | Average optical flow motion |
| max_motion | DOUBLE | Maximum optical flow motion |
| horizontal_motion | DOUBLE | Side-to-side movement estimate |
| vertical_motion | DOUBLE | Up/down movement estimate |
| terrain_label | TEXT | Smooth, rough, very rough |
| turn_direction | TEXT | Left, right, straight |
| highlight_score | DOUBLE | Combined score for interesting moments |
| created_at | TIMESTAMP | Record creation timestamp |

## Table: highlight_events

| Column | Type | Description |
|---|---|---|
| event_id | INTEGER | Unique event identifier |
| video_id | INTEGER | Related video |
| start_seconds | DOUBLE | Event start time |
| end_seconds | DOUBLE | Event end time |
| event_type | TEXT | Event label such as fast_section, rough_section, jump, drop, turn |
| confidence | DOUBLE | Confidence score |
| highlight_score | DOUBLE | Event importance score |
| notes | TEXT | Optional notes |
| created_at | TIMESTAMP | Record creation timestamp |

## Table: extracted_frames

| Column | Type | Description |
|---|---|---|
| frame_id | INTEGER | Unique extracted frame identifier |
| video_id | INTEGER | Related video |
| timestamp_seconds | DOUBLE | Timestamp where frame was extracted |
| frame_path | TEXT | Saved image path |
| reason | TEXT | Why the frame was extracted |
| score | DOUBLE | Highlight or motion score |
| created_at | TIMESTAMP | Record creation timestamp |
