## 3. `docs/class_diagram.md`

```markdown
# TrailVision Class Diagram

```text
┌──────────────────────────────┐
│            Ride              │
├──────────────────────────────┤
│ ride_id                      │
│ ride_name                    │
│ ride_date                    │
│ location                     │
│ trail_name                   │
│ notes                        │
│ videos                       │
├──────────────────────────────┤
│ add_video()                  │
│ video_count()                │
│ summary()                    │
└───────────────┬──────────────┘
                │ 1-to-many
                ▼
┌──────────────────────────────┐
│            Video             │
├──────────────────────────────┤
│ video_id                     │
│ ride_id                      │
│ original_path                │
│ converted_path               │
│ duration_seconds             │
│ fps                          │
│ frame_count                  │
│ width                        │
│ height                       │
├──────────────────────────────┤
│ original_filename            │
│ converted_filename           │
│ has_conversion()             │
│ summary()                    │
└──────────────────────────────┘
