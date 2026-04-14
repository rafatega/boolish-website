from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoordToGeohashInput:
    raw_coords: str
    target_precision: int
    max_outside: float


@dataclass(frozen=True)
class CoordToGeohashOutput:
    geohashes: list[str]
    geohash_count: int
    rings_count: int
    stats_by_length: dict[int, int]
    map_html: str
    excel_bytes: bytes
