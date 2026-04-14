from __future__ import annotations

from typing import Optional

from app.modules.coord_to_geohash.domain.errors import CoordToGeohashValidationError

Point = tuple[float, float]
Ring = list[Point]


class CoordinateParser:
    def parse(self, raw_coords: str) -> list[Point]:
        points: list[Point] = []
        for raw_line in raw_coords.strip().splitlines():
            line = raw_line.strip()
            if not line:
                continue

            parts = [part.strip() for part in line.split(",")]
            if len(parts) != 2:
                raise CoordToGeohashValidationError(
                    f"Linha invalida: '{line}'. Esperado formato 'lon, lat'."
                )

            try:
                lon = float(parts[0])
                lat = float(parts[1])
            except ValueError as exc:
                raise CoordToGeohashValidationError(
                    f"Linha invalida: '{line}'. Longitude e latitude devem ser numericas."
                ) from exc

            points.append((lon, lat))

        if len(points) < 4:
            raise CoordToGeohashValidationError(
                "Sao necessarios ao menos 4 pontos para formar um anel."
            )

        return points


class RingDetector:
    def __init__(self, close_tolerance: float = 1e-7) -> None:
        self._close_tolerance = close_tolerance

    def detect(self, points: list[Point]) -> list[Ring]:
        rings: list[Ring] = []
        current_ring: Ring = []
        start: Optional[Point] = None

        for point in points:
            if not current_ring:
                current_ring = [point]
                start = point
                continue

            current_ring.append(point)
            if start is not None and len(current_ring) >= 4 and self._is_close(point, start):
                current_ring[-1] = start
                rings.append(current_ring)
                current_ring = []
                start = None

        if current_ring and start is not None and len(current_ring) >= 4:
            if current_ring[0] != current_ring[-1]:
                current_ring.append(current_ring[0])
            rings.append(current_ring)

        if not rings:
            raise CoordToGeohashValidationError(
                "Nenhum anel foi detectado. Confira se o contorno esta fechado."
            )

        return rings

    def _is_close(self, point_a: Point, point_b: Point) -> bool:
        return (
            abs(point_a[0] - point_b[0]) <= self._close_tolerance
            and abs(point_a[1] - point_b[1]) <= self._close_tolerance
        )
