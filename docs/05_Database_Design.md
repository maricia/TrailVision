# TrailVision Database ERD

```text
┌──────────────┐
│    rides     │
├──────────────┤
│ ride_id PK   │
│ ride_name    │
│ ride_date    │
│ location     │
│ trail_name   │
│ notes        │
└──────┬───────┘
       │ 1-to-many
       ▼
┌──────────────┐
│    videos    │
├──────────────┤
│ video_id PK  │
│ ride_id FK   │
│ filename     │
│ path         │
│ duration     │
│ fps          │
│ frame_count  │
│ width        │
│ height       │
└──────┬───────┘
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌──────────────────┐  ┌────────────────────┐
│ frame_metrics    │  │ video_conversions  │
├──────────────────┤  ├────────────────────┤
│ metric_id PK     │  │ conversion_id PK   │
│ video_id FK      │  │ video_id FK        │
│ timestamp        │  │ converted_path     │
│ avg_motion       │  │ codec              │
│ max_motion       │  │ status             │
│ highlight_score  │  └────────────────────┘
└──────────────────┘

       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│ highlight_events │  │ extracted_frames │
├──────────────────┤  ├──────────────────┤
│ event_id PK      │  │ frame_id PK      │
│ video_id FK      │  │ video_id FK      │
│ start_seconds    │  │ timestamp        │
│ end_seconds      │  │ frame_path       │
│ event_type       │  │ reason           │
│ confidence       │  │ score            │
└──────────────────┘  └──────────────────┘
