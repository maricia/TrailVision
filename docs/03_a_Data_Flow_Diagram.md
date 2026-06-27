# TrailVision Data Flow Diagram

```text
Step 1: Import

Raw GoPro MP4
      ↓
VideoService
      ↓
Video metadata

Step 2: Convert

Raw GoPro MP4
      ↓
FFmpeg
      ↓
Converted MP4

Step 3: Analyze

Converted MP4
      ↓
OpenCV
      ↓
Motion metrics
      ↓
Optical flow metrics
      ↓
Highlight scores

Step 4: Extract

Highlight timestamps
      ↓
Frame extraction
      ↓
JPG highlight images

Step 5: Store

Ride object
Video object
Frame metrics
Highlight events
Extracted frames
      ↓
DuckDB

Step 6: Model

DuckDB raw tables
      ↓
dbt staging models
      ↓
dbt analytics models

Step 7: Report

Analytics tables
      ↓
Power BI
      ↓
Ride dashboard
