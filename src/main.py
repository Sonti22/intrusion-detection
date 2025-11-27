"""Main application entry point for intrusion detection."""
import time

import cv2

from .adapters.json_zone_repository import JsonZoneRepository
from .adapters.opencv_ui import OpenCVFrameRenderer
from .adapters.yolo_detector import YoloPersonDetector
from .config import ALARM_COOLDOWN_SECONDS, VIDEO_PATH, WINDOW_NAME
from .core.services import IntrusionService


def run() -> None:
    """Run main detection loop."""
    repo = JsonZoneRepository()
    zones = repo.load_zones()
    if not zones:
        print("No restricted zones defined. Run `python -m src.tools.mark_restricted_zone` first.")
        return

    detector = YoloPersonDetector()
    renderer = OpenCVFrameRenderer()
    service = IntrusionService(zones=zones, cooldown_seconds=ALARM_COOLDOWN_SECONDS)

    cap = cv2.VideoCapture(str(VIDEO_PATH))
    if not cap.isOpened():
        print(f"Cannot open video: {VIDEO_PATH}")
        return

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            timestamp = time.time()
            detections = detector.detect(frame, timestamp)
            state = service.update(detections, timestamp)
            frame_out = renderer.render(frame, zones, detections, state)
            cv2.imshow(WINDOW_NAME, frame_out)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):  # q or ESC
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run()

