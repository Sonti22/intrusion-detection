"""JSON-based repository for restricted zones with improved robustness."""
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
    """JSON file‑based implementation of :class:`ZoneRepository`.

    The original implementation raised uncaught exceptions when the JSON file
    was malformed and assumed the destination directory already existed when
    saving. Both behaviours could crash the application at runtime. This version
    adds defensive handling:

    * Returns an empty list and logs a warning if the JSON cannot be decoded.
    * Guarantees the parent directory exists before writing.
    """

    def __init__(self, path: Path | None = None) -> None:
        """Initialize repository with a JSON file path.

        Args:
            path: Optional custom path; defaults to :data:`ZONES_PATH` from the
                configuration module.
        """
        self._path = path or ZONES_PATH

    def load_zones(self) -> list[Zone]:
        """Load zones from a JSON file.

        Returns:
            A list of :class:`Zone` objects. If the file does not exist, is empty,
            or contains invalid JSON, an empty list is returned and a warning is
            logged.
        """
        if not self._path.exists():
            return []

        raw = self._path.read_text(encoding="utf-8").strip()
        if not raw:
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            _logger.warning("Failed to decode zones JSON %s: %s", self._path, exc)
            return []

        zones: list[Zone] = []
        for item in data:
            # Defensive conversion – ensure points are integer tuples
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
        """Save zones to a JSON file.

        The method creates the parent directory if it does not exist, then writes
        a pretty‑printed JSON payload.
        """
        # Ensure the directory hierarchy is present to avoid IOError.
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
