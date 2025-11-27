"""OpenCV-based frame renderer adapter."""
from __future__ import annotations

import cv2
import numpy as np

from ..core.entities import Detection, IntrusionState, Zone, bbox_center
from ..core.ports import FrameRenderer


class OpenCVFrameRenderer(FrameRenderer):
    """OpenCV-based implementation of FrameRenderer."""

    def render(
        self,
        frame: np.ndarray,
        zones: list[Zone],
        detections: list[Detection],
        state: IntrusionState,
    ) -> np.ndarray:
        """Render frame with zones, detections, and alarm overlay.

        Args:
            frame: Original video frame
            zones: List of restricted zones to draw
            detections: List of detected persons
            state: Current intrusion detection state

        Returns:
            Rendered frame with overlays
        """
        output = frame.copy()

        # Draw zones (yellow)
        for z in zones:
            pts = np.array(z.points, dtype=np.int32)
            cv2.polylines(output, [pts], isClosed=True, color=(0, 255, 255), thickness=2)
            x, y = z.points[0]
            cv2.putText(
                output,
                z.name,
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

        # Draw detections (green bbox, blue center)
        for det in detections:
            x1, y1, x2, y2 = det.bbox
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cx, cy = bbox_center(det.bbox)
            cv2.circle(output, (cx, cy), 3, (255, 0, 0), -1)

        # Draw alarm (red text)
        if state.alarm_active:
            h, w = output.shape[:2]
            cv2.putText(
                output,
                "ALARM!",
                (int(w * 0.35), 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3,
            )

        return output

