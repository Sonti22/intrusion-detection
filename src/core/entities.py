"""Core domain entities for intrusion detection."""
from dataclasses import dataclass
from typing import Optional, Set, Tuple

Point = Tuple[int, int]
BBox = Tuple[int, int, int, int]  # x1, y1, x2, y2


@dataclass
class Zone:
    """Represents a restricted zone as a polygon."""

    id: str
    name: str
    points: list[Point]


@dataclass
class Detection:
    """Represents a detected person in a frame."""

    id: Optional[int]  # None if tracking is not used
    label: str  # expected "person"
    score: float
    bbox: BBox


@dataclass
class IntrusionState:
    """Current state of intrusion detection system."""

    timestamp: float
    alarm_active: bool
    zones_with_intruders: Set[str]


def bbox_center(bbox: BBox) -> Point:
    """Calculate the center point of a bounding box.

    Args:
        bbox: Bounding box as (x1, y1, x2, y2)

    Returns:
        Center point as (x, y)
    """
    x1, y1, x2, y2 = bbox
    return (int((x1 + x2) / 2), int((y1 + y2) / 2))

