'''JSON-based repository for restricted zones.'''
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

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

    def load_zones(self) -> list[Zone]:
        """Load zones from JSON file.

        Returns:
            List of zones. Empty list if file doesn't exist, is empty, or cannot be parsed.
        """
        if not self._path.exists():
            return []

        raw = self._path.read_text(encoding="utf-8").strip()
        if not raw:
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            _logger.error("Failed to decode zones JSON %s: %s", self._path, exc)
            return []

        zones: list[Zone] = []
        for item in data:
            try:
                points_raw = item["points"]
                # Ensure each point is a two‑element iterable of ints
                points: list[Point] = [tuple(map(int, p)) for p in points_raw]
                zones.append(
                    Zone(
                        id=str(item["id"]),
                        name=str(item.get("name", item["id"])),
                        points=points,
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                _logger.warning(
                    "Skipping malformed zone entry %s in %s: %s", item, self._path, exc
                )
                continue
        return zones

    def save_zones(self, zones: list[Zone]) -> None:
        """Save zones to JSON file.

        Args:
            zones: List of zones to save
        """
        # Ensure the directory exists before writing
        self._path.parent.mkdir(parents=True, exist_ok=True)

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
