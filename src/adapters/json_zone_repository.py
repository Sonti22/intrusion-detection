"""JSON-based repository for restricted zones."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core.entities import Point, Zone
from ..core.ports import ZoneRepository
from ..config import ZONES_PATH


class JsonZoneRepository(ZoneRepository):
    """JSON file-based implementation of ZoneRepository."""

    def __init__(self, path: Path | None = None) -> None:
        """Initialize repository with JSON file path.

        Args:
            path: Path to JSON file. Defaults to ZONES_PATH from config.
        """
        self._path = path or ZONES_PATH

    def load_zones(self) -> list[Zone]:
        """Load zones from JSON file.

        Returns:
            List of zones. Empty list if file doesn't exist or is empty.
        """
        if not self._path.exists():
            return []

        raw = self._path.read_text(encoding="utf-8").strip()
        if not raw:
            return []

        data = json.loads(raw)
        zones: list[Zone] = []
        for item in data:
            points: list[Point] = [tuple(map(int, p)) for p in item["points"]]
            zones.append(
                Zone(
                    id=str(item["id"]),
                    name=str(item.get("name", item["id"])),
                    points=points,
                )
            )
        return zones

    def save_zones(self, zones: list[Zone]) -> None:
        """Save zones to JSON file.

        Args:
            zones: List of zones to save
        """
        payload: list[dict[str, Any]] = []
        for z in zones:
            payload.append(
                {
                    "id": z.id,
                    "name": z.name,
                    "points": [[int(x), int(y)] for (x, y) in z.points],
                }
            )
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

