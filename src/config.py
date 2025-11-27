"""Configuration settings for intrusion detection system."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

VIDEO_PATH = DATA_DIR / "test.mp4"
ZONES_PATH = ROOT_DIR / "restricted_zones.json"

MODEL_NAME = "yolov8n.pt"
DEVICE = "cpu"  # can be changed to "cuda"

CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45
ALARM_COOLDOWN_SECONDS = 3.0
WINDOW_NAME = "Intrusion detection"

