"""Interactive tool for marking restricted zones on video frame."""
from __future__ import annotations

import cv2
import numpy as np

from ..adapters.json_zone_repository import JsonZoneRepository
from ..config import VIDEO_PATH

# Global state for mouse callback
current_points: list[tuple[int, int]] = []
drawing = False
frame_copy: np.ndarray | None = None
window_name = "Mark Restricted Zone"


def mouse_callback(event: int, x: int, y: int, flags: int, param: None) -> None:
    """Handle mouse events for point selection.

    Args:
        event: OpenCV mouse event type
        x: Mouse x coordinate
        y: Mouse y coordinate
        flags: Event flags
        param: User data (unused)
    """
    global current_points, drawing, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        current_points.append((x, y))
        drawing = True
        _redraw_frame()

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        _redraw_frame()
        if current_points:
            # Draw line to current mouse position
            temp_frame = frame_copy.copy()
            pts = np.array(current_points + [(x, y)], dtype=np.int32)
            if len(pts) > 1:
                cv2.polylines(temp_frame, [pts], isClosed=False, color=(0, 255, 255), thickness=2)
            for pt in current_points:
                cv2.circle(temp_frame, pt, 5, (0, 255, 0), -1)
            cv2.imshow(window_name, temp_frame)


def _redraw_frame() -> None:
    """Redraw frame with current polygon."""
    global frame_copy, current_points

    if frame_copy is None:
        return

    temp_frame = frame_copy.copy()
    if len(current_points) > 1:
        pts = np.array(current_points, dtype=np.int32)
        cv2.polylines(temp_frame, [pts], isClosed=True, color=(0, 255, 255), thickness=2)
    for pt in current_points:
        cv2.circle(temp_frame, pt, 5, (0, 255, 0), -1)
    cv2.imshow(window_name, temp_frame)


def main() -> None:
    """Main function for zone markup tool."""
    global current_points, frame_copy

    # Load first frame from video
    cap = cv2.VideoCapture(str(VIDEO_PATH))
    if not cap.isOpened():
        print(f"Cannot open video: {VIDEO_PATH}")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Cannot read first frame from video")
        return

    frame_copy = frame.copy()
    current_points = []

    # Create window and set mouse callback
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("Instructions:")
    print("  - Left click to add points to polygon")
    print("  - Press 's' to save zone")
    print("  - Press 'r' to reset current polygon")
    print("  - Press 'q' or ESC to quit without saving")

    while True:
        cv2.imshow(window_name, frame_copy)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            if len(current_points) < 3:
                print("Need at least 3 points to form a polygon")
                continue

            # Save zone
            repo = JsonZoneRepository()
            from ..core.entities import Zone

            zones = repo.load_zones()
            new_zone = Zone(
                id="zone_1",
                name="Restricted area 1",
                points=current_points,
            )
            # Replace existing zone_1 or add new
            zones = [z for z in zones if z.id != "zone_1"]
            zones.append(new_zone)
            repo.save_zones(zones)
            print(f"Zone saved with {len(current_points)} points")
            break

        elif key == ord("r"):
            current_points = []
            frame_copy = frame.copy()
            cv2.imshow(window_name, frame_copy)
            print("Polygon reset")

        elif key in (ord("q"), 27):  # q or ESC
            print("Exiting without saving")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

