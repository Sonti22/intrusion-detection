'''JSON-based repository for restricted zones.'''
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, List

from ..core.entities import Point, Zone
from ..core.ports import ZoneRepository
from ..config import ZONES_PATH

_logger = logging.getLogger(__name__)


class JsonZoneRepository(ZoneRepository):
    """JSON file-based implementation of ZoneRepository."""

    def __init__(self, path: Path | None = None) -> None:
        """Initialize repository with JSON file path.

        Args:
            path: Path to JSON file. Defaults to ZONES_PATH from config.
        """
        self._path = path or ZONES_PATH

    def load_zones(self) -> List[Zone]:
        """Load zones from JSON file.

        Returns:
            List of zones. Empty list if file doesn't exist, is empty, or contains no
            valid zone definitions.
        """
        if not self._path.exists():
            _logger.debug("Zone file %s does not exist; returning empty list.", self._path)
            return []

        raw = self._path.read_text(encoding="utf-8").strip()
        if not raw:
            _logger.debug("Zone file %s is empty; returning empty list.", self._path)
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            _logger.error("Failed to parse JSON from %s: %s", self._path, exc)
            return []

        zones: List[Zone] = []
        for idx, item in enumerate(data):
            try:
                zone_id = str(item["id"])  # mandatory
                points_raw = item["points"]  # mandatory
                # Convert each point to a tuple of ints
                points: List[Point] = []
                for p in points_raw:
                    try:
                        pt = tuple(map(int, p))
                        if len(pt) != 2:
                            raise ValueError("Point must have exactly two coordinates")
                        points.append(pt)
                    except Exception as e:
                        raise ValueError(f"Invalid point {p}: {e}")
                if len(points) < 3:
                    raise ValueError("A zone must have at least three points to form a polygon")
                name = str(item.get("name", zone_id))
                zones.append(Zone(id=zone_id, name=name, points=points))
            except Exception as e:
                _logger.warning(
                    "Skipping invalid zone entry at index %d in %s: %s", idx, self._path, e
                )
                continue
        return zones

    def save_zones(self, zones: List[Zone]) -> None:
        """Save zones to JSON file.

        Args:
            zones: List of zones to save
        """
        payload: List[dict[str, Any]] = []
        for z in zones:
            payload.append(
                {
                    "id": z.id,
                    "name": z.name,
                    "points": [[int(x), int(y)] for (x, y) in z.points],
                }
            )
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
