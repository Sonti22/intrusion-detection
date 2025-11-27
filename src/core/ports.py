"""Protocol interfaces for adapters (ports in hexagonal architecture)."""
from typing import Protocol

import numpy as np

from .entities import Detection, IntrusionState, Zone


class PersonDetector(Protocol):
    """Interface for person detection on video frames."""

    def detect(self, frame: np.ndarray, timestamp: float) -> list[Detection]:
        """Detect all persons in the frame.

        Args:
            frame: Video frame as numpy array
            timestamp: Current frame timestamp

        Returns:
            List of detected persons
        """


class ZoneRepository(Protocol):
    """Interface for loading restricted zones from persistent storage."""

    def load_zones(self) -> list[Zone]:
        """Load zones from persistent storage.

        Returns:
            List of restricted zones
        """


class FrameRenderer(Protocol):
    """Interface for rendering frames with zones, detections, and alarm state."""

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

