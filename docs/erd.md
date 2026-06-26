# TrailVision Entity Relationship Diagram

```text
rides
  |
  | 1-to-many
  v
videos
  |
  | 1-to-many
  v
video_conversions

videos
  |
  | 1-to-many
  v
frame_metrics

videos
  |
  | 1-to-many
  v
highlight_events

videos
  |
  | 1-to-many
  v
extracted_frames