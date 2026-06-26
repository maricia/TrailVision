# Project TrailVision

TrailVision is a mountain bike video analytics platform that converts GoPro footage into ride metrics, highlight moments, extracted frames, and dashboard-ready data.

## Problem

Mountain bike videos are hard to review manually. A short ride can create thousands of frames, and finding the best moments takes time.

## Solution

TrailVision uses Python, FFmpeg, OpenCV, DuckDB, and future dbt/Power BI models to automate ride analysis.

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
- dbt planned
- Power BI planned
- Tkinter planned

## Project Structure

```text
MTB_Video_Analytics
├── app
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

##Pipeline

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


## 2. `docs/system_architecture_diagram.md`

```markdown
# TrailVision System Architecture Diagram

```text
                         Project TrailVision
┌──────────────────────────────────────────────────────────────┐
│                         Desktop App                          │
│                    app/main.py - future GUI                   │
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
│       Vision Layer       │   │          Models Layer          │
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
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                    Analytics / Reporting                     │
│                                                              │
│   dbt models - planned                                       │
│   Power BI dashboard - planned                               │
└──────────────────────────────────────────────────────────────┘




