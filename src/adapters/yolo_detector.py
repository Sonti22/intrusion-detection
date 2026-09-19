'''YOLO-based person detector adapter.'''
from __future__ import annotations

import numpy as np
from ultralytics import YOLO

from ..core.entities import BBox, Detection
from ..core.ports import PersonDetector
from ..config import CONFIDENCE_THRESHOLD, DEVICE, IOU_THRESHOLD, MODEL_NAME


class YoloPersonDetector(PersonDetector):
    """YOLO-based implementation of PersonDetector.

    The constructor now validates that the specified model can be loaded.
    If loading fails (e.g., missing file, corrupted weights), a clear
    ``RuntimeError`` is raised with the original exception attached as the
    cause. This prevents the application from crashing later with an obscure
    ``ImportError`` or ``AttributeError`` when ``detect`` is called.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        device: str = DEVICE,
        conf: float = CONFIDENCE_THRESHOLD,
        iou: float = IOU_THRESHOLD,
    ) -> None:
        """Initialize YOLO detector.

        Args:
            model_name: YOLO model name or path.
            device: Device to run on ("cpu" or "cuda").
            conf: Confidence threshold.
            iou: IoU threshold for NMS.
        """
        try:
            self.model = YOLO(model_name)
        except Exception as exc:  # pragma: no cover – defensive guard
            raise RuntimeError(
                f"Failed to load YOLO model '{model_name}'. Ensure the model file exists "
                "and is compatible with the installed ultralytics package."
            ) from exc
        self.device = device
        self.conf = conf
        self.iou = iou

    def detect(self, frame: np.ndarray, timestamp: float) -> list[Detection]:
        """Detect persons in frame using YOLO.

        Args:
            frame: Video frame as numpy array.
            timestamp: Current frame timestamp (unused but required by protocol).

        Returns:
            List of detected persons.
        """
        results = self.model(
            frame,
            device=self.device,
            conf=self.conf,
            iou=self.iou,
            verbose=False,
        )
        detections: list[Detection] = []
        for r in results:
            names = r.names
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0].item())
                label = names[cls_id]
                if label != "person":
                    continue
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                bbox: BBox = (int(x1), int(y1), int(x2), int(y2))
                score = float(box.conf[0].item())
                detections.append(
                    Detection(
                        id=None,
                        label=label,
                        score=score,
                        bbox=bbox,
                    )
                )
        return detections
