# Intrusion Detection System

A video-based intrusion detection system that uses YOLO to detect people entering restricted zones. The system monitors video frames, detects persons using YOLOv8, checks if they are inside predefined restricted zones, and triggers an alarm with a cooldown mechanism.

## Features

- **Person Detection**: Uses YOLOv8 to detect people in video frames
- **Zone Markup**: Interactive tool to mark restricted zones as polygons
- **Intrusion Detection**: Real-time detection of people entering restricted zones
- **Alarm System**: Visual alarm with 3-second cooldown after person exits zone
- **Clean Architecture**: Separated core logic from adapters (hexagonal architecture)

## Requirements

- Python 3.11+
- ffmpeg (optional, for video processing)

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Place your test video in `data/test.mp4`

## Usage

### Step 1: Mark Restricted Zone

First, you need to mark the restricted zone on a video frame:

```bash
python -m src.tools.mark_restricted_zone
```

**Instructions:**
- Left-click to add points to the polygon
- Press `s` to save the zone
- Press `r` to reset the current polygon
- Press `q` or `ESC` to quit without saving

The zone will be saved to `restricted_zones.json`.

### Step 2: Run Detection

Start the intrusion detection system:

```bash
python -m src.main
```

The system will:
- Load restricted zones from `restricted_zones.json`
- Process video frames and detect people using YOLO
- Check if detected people are inside restricted zones
- Display visual alarm when intrusion is detected
- Press `q` or `ESC` to exit

## Alarm Behavior

- **Activation**: Alarm activates immediately when a person enters a restricted zone
- **Deactivation**: Alarm deactivates 3 seconds (`ALARM_COOLDOWN_SECONDS`) after the last person exits all restricted zones
- **Visual Indicator**: Red "ALARM!" text appears at the top of the frame when active

## Architecture

The project follows clean architecture principles:

- **Core Layer** (`src/core/`): Domain entities, ports (interfaces), and business logic
  - `entities.py`: Zone, Detection, IntrusionState
  - `ports.py`: Protocol interfaces for adapters
  - `services.py`: IntrusionService with cooldown logic

- **Adapters Layer** (`src/adapters/`): External dependencies implementations
  - `yolo_detector.py`: YOLO person detection
  - `json_zone_repository.py`: JSON file-based zone storage
  - `opencv_ui.py`: OpenCV frame rendering

- **Tools** (`src/tools/`): Utility scripts
  - `mark_restricted_zone.py`: Interactive zone markup tool

## Configuration

Edit `src/config.py` to adjust:

- `VIDEO_PATH`: Path to input video file
- `ZONES_PATH`: Path to zones JSON file
- `MODEL_NAME`: YOLO model name (default: "yolov8n.pt")
- `DEVICE`: "cpu" or "cuda"
- `CONFIDENCE_THRESHOLD`: Detection confidence threshold (default: 0.5)
- `IOU_THRESHOLD`: IoU threshold for NMS (default: 0.45)
- `ALARM_COOLDOWN_SECONDS`: Cooldown period in seconds (default: 3.0)

## Project Structure

```
intrusion-detection/
├── data/
│   └── test.mp4              # Input video file
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── main.py               # Main application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── entities.py       # Domain entities
│   │   ├── ports.py          # Protocol interfaces
│   │   └── services.py       # Business logic
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── yolo_detector.py  # YOLO detection adapter
│   │   ├── json_zone_repository.py  # Zone storage
│   │   └── opencv_ui.py      # Frame rendering
│   └── tools/
│       ├── __init__.py
│       └── mark_restricted_zone.py  # Zone markup tool
├── restricted_zones.json     # Stored zone definitions
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## License

MIT

