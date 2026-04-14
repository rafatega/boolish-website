from __future__ import annotations

from dataclasses import dataclass

from app.dependencies import coord_to_geohash_use_case
from app.modules.coord_to_geohash.domain.models import CoordToGeohashInput


@dataclass(frozen=True)
class CoordToGeohashResult:
    geohashes: list[str]
    geohash_count: int
    rings_count: int
    stats_by_length: dict[int, int]
    map_html: str
    excel_bytes: bytes


def run_coord_to_geohash(raw_coords: str, target_precision: int, max_outside: float) -> CoordToGeohashResult:
    output = coord_to_geohash_use_case.execute(
        CoordToGeohashInput(
            raw_coords=raw_coords,
            target_precision=target_precision,
            max_outside=max_outside,
        )
    )

    return CoordToGeohashResult(
        geohashes=output.geohashes,
        geohash_count=output.geohash_count,
        rings_count=output.rings_count,
        stats_by_length=output.stats_by_length,
        map_html=output.map_html,
        excel_bytes=output.excel_bytes,
    )
