"""Core service for intrusion detection with cooldown logic."""
from __future__ import annotations

from .entities import Detection, IntrusionState, Point, Zone, bbox_center


def point_in_polygon(point: Point, polygon: list[Point]) -> bool:
    """Check if a point is inside a polygon using ray-casting algorithm.

    Args:
        point: Point to check (x, y)
        polygon: List of polygon vertices

    Returns:
        True if point is inside polygon, False otherwise
    """
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


class IntrusionService:
    """Service for detecting intrusions into restricted zones with cooldown."""

    def __init__(self, zones: list[Zone], cooldown_seconds: float) -> None:
        """Initialize intrusion service.

        Args:
            zones: List of restricted zones to monitor
            cooldown_seconds: Cooldown period after last intrusion before alarm deactivates
        """
        self.zones = zones
        self.cooldown_seconds = cooldown_seconds
        self.alarm_active: bool = False
        self.last_time_without_intruders: float | None = None

    def update(self, detections: list[Detection], timestamp: float) -> IntrusionState:
        """Update intrusion state based on current detections.

        Args:
            detections: List of detected persons
            timestamp: Current timestamp

        Returns:
            Current intrusion state
        """
        zones_with_intruders: set[str] = set()

        # Check each detection against each zone
        for det in detections:
            center = bbox_center(det.bbox)
            for zone in self.zones:
                if point_in_polygon(center, zone.points):
                    zones_with_intruders.add(zone.id)

        # Update alarm state
        if zones_with_intruders:
            # At least one zone has intruders
            self.alarm_active = True
            self.last_time_without_intruders = None
        else:
            # No zones have intruders
            if self.alarm_active:
                if self.last_time_without_intruders is None:
                    self.last_time_without_intruders = timestamp
                elif timestamp - self.last_time_without_intruders >= self.cooldown_seconds:
                    self.alarm_active = False
                    self.last_time_without_intruders = None

        return IntrusionState(
            timestamp=timestamp,
            alarm_active=self.alarm_active,
            zones_with_intruders=zones_with_intruders,
        )


def _self_test() -> None:
    """Self-test function for manual testing."""
    from .entities import BBox, Detection, Zone

    # Test 1: Simple intrusion detection
    zone1 = Zone(
        id="zone_1",
        name="Test Zone",
        points=[(100, 100), (200, 100), (200, 200), (100, 200)],
    )
    service = IntrusionService(zones=[zone1], cooldown_seconds=3.0)

    # Person inside zone
    det1 = Detection(
        id=None, label="person", score=0.9, bbox=(150, 150, 170, 180)  # center at (160, 165)
    )
    state1 = service.update([det1], timestamp=1.0)
    assert state1.alarm_active is True, "Alarm should be active when person is in zone"
    assert "zone_1" in state1.zones_with_intruders, "zone_1 should be in zones_with_intruders"

    # Person outside zone
    det2 = Detection(
        id=None, label="person", score=0.9, bbox=(250, 250, 270, 280)  # center at (260, 265)
    )
    state2 = service.update([det2], timestamp=2.0)
    assert state2.alarm_active is True, "Alarm should still be active (cooldown)"
    assert len(state2.zones_with_intruders) == 0, "No zones should have intruders"

    # After cooldown
    state3 = service.update([], timestamp=5.1)  # 3.1 seconds after last intrusion
    assert state3.alarm_active is False, "Alarm should be inactive after cooldown"

    print("✓ All self-tests passed!")


if __name__ == "__main__":
    _self_test()

