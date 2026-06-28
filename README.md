# TrailVision

TrailVision is a mountain bike video analytics platform that converts GoPro footage into ride metrics, highlight moments, extracted frames, and dashboard-ready data.

## Problem

Manual review of mountain bike video is slow. A short ride can create thousands of frames, making it hard to find the best moments.

## Solution

TrailVision automates ride analysis using Python, FFmpeg, OpenCV, DuckDB, and planned dbt/Power BI reporting.

![Terrain Classification Distribution](charts/03_terrain_distribution.png)
![highlight_by_directionalt text](charts/05_highlight_by_direction.png)
![motion_vs_highlightalt text](charts/06_motion_vs_highlight.png)
![top_highlight_moments](charts/07_top_highlight_moments.png)

## Current Features

- Convert GoPro video to analysis-ready MP4
- Read video metadata
- Calculate motion metrics
- Run optical flow analysis
- Extract highlight frames
- Store project data in DuckDB
- Use object-oriented models for rides and videos

## Tech Stack

- Python
- OpenCV
- FFmpeg
- DuckDB
- dbt (planned)
- Power BI (planned)
- Tkinter (planned)

## Project Structure

```text
MTB_Video_Analytics
├── app
├── charts
├── converted
├── database
├── docs
├── frames
├── models
├── output
├── raw_videos
├── scripts
├── services
├── tests
└── vision
```

## Pipeline

```text
Raw GoPro Video
      ↓
FFmpeg Conversion
      ↓
OpenCV Analysis
      ↓
Motion + Optical Flow Metrics
      ↓
Highlight Extraction
      ↓
DuckDB
      ↓
dbt
      ↓
Power BI
```

## Architecture

The project is structured with a desktop app layer, a services layer, vision and model layers, and a data layer.

### System architecture diagram

```text
                         Project TrailVision
┌──────────────────────────────────────────────────────────────┐
│                         Desktop App                          │
│                    app/main.py - future GUI                  │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                         Services Layer                       │
│                                                              │
│   VideoService        AnalysisService        DatabaseService │
│   - metadata          - motion metrics       - rides         │
│   - conversion        - optical flow         - videos        │
│   - file paths        - highlights           - metrics       │
└───────────────┬──────────────────────┬───────────────────────┘
                │                      │
                ▼                      ▼
┌──────────────────────────┐   ┌───────────────────────────────┐
│       Vision Layer       │   │          Models Layer         │
│                          │   │                               │
│   motion.py              │   │   Ride                        │
│   optical_flow.py        │   │   Video                       │
│   highlights.py          │   │   Future: Metric, Highlight   │
└───────────────┬──────────┘   └───────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│                                                              │
│   DuckDB                                                     │
│   database/trailvision.duckdb                                │
└──────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    Analytics / Reporting                     │
│                                                              │
│   dbt models - planned                                       │
│   Power BI dashboard - planned                               │
└──────────────────────────────────────────────────────────────┘
```

