from __future__ import annotations

import pygeohash as pgh
from shapely.geometry import box
from shapely.prepared import prep

from app.modules.coord_to_geohash.domain.errors import CoordToGeohashValidationError

_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


class GeohashCoverageService:
    def calculate(self, geometry, target_precision: int, max_outside: float) -> set[str]:
        if not (0.0 <= max_outside <= 1.0):
            raise CoordToGeohashValidationError("max_outside deve estar entre 0 e 1.")
        if target_precision < 4:
            raise CoordToGeohashValidationError("target_precision deve ser maior ou igual a 4.")

        prepared_geometry = prep(geometry)
        min_lon, min_lat, max_lon, max_lat = geometry.bounds
        seed_codes = self._seed_cover(min_lon, min_lat, max_lon, max_lat, precision=4)

        accepted_codes: set[str] = set()
        stack = list(seed_codes)

        while stack:
            code = stack.pop()
            cell = self._cell_geometry(code)

            if prepared_geometry.disjoint(cell):
                continue

            if len(code) < target_precision:
                stack.extend(self._children(code))
                continue

            intersection = geometry.intersection(cell)
            if intersection.is_empty:
                continue

            inside_ratio = intersection.area / cell.area
            outside_ratio = 1.0 - inside_ratio
            if outside_ratio <= max_outside:
                accepted_codes.add(code)

        return accepted_codes

    def _seed_cover(
        self,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float,
        precision: int,
    ) -> set[str]:
        bbox = box(min_lon, min_lat, max_lon, max_lat)
        center_lon = (min_lon + max_lon) / 2.0
        center_lat = (min_lat + max_lat) / 2.0
        start = self._encode(center_lat, center_lon, precision)

        visited: set[str] = set()
        result: set[str] = set()
        stack = [start]

        while stack:
            code = stack.pop()
            if code in visited:
                continue
            visited.add(code)

            cell = self._cell_geometry(code)
            if not cell.intersects(bbox):
                continue

            result.add(code)
            for neighbor in self._neighbors(code).values():
                if neighbor not in visited:
                    stack.append(neighbor)

        return result

    def _neighbors(self, code: str) -> dict[str, str]:
        min_lon, min_lat, max_lon, max_lat = self._bbox(code)
        dx = max_lon - min_lon
        dy = max_lat - min_lat
        cx = (min_lon + max_lon) / 2.0
        cy = (min_lat + max_lat) / 2.0
        precision = len(code)

        return {
            "n": self._encode(cy + dy, cx, precision),
            "ne": self._encode(cy + dy, cx + dx, precision),
            "e": self._encode(cy, cx + dx, precision),
            "se": self._encode(cy - dy, cx + dx, precision),
            "s": self._encode(cy - dy, cx, precision),
            "sw": self._encode(cy - dy, cx - dx, precision),
            "w": self._encode(cy, cx - dx, precision),
            "nw": self._encode(cy + dy, cx - dx, precision),
        }

    def _children(self, code: str) -> list[str]:
        return [code + char for char in _BASE32]

    def _bbox(self, code: str) -> tuple[float, float, float, float]:
        lat, lon, lat_err, lon_err = pgh.decode_exactly(code)
        return (lon - lon_err, lat - lat_err, lon + lon_err, lat + lat_err)

    def _cell_geometry(self, code: str):
        return box(*self._bbox(code))

    def _encode(self, lat: float, lon: float, precision: int) -> str:
        return pgh.encode(lat, lon, precision=precision)
