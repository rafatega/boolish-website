from __future__ import annotations

from pydantic import BaseModel, Field


class CoordToGeohashRunRequest(BaseModel):
    raw_coords: str = Field(..., description="Coordenadas no formato lon, lat em linhas separadas.")
    target_precision: int = Field(5, ge=4, le=12, description="Precisao final do geohash.")
    max_outside: float = Field(1.0, ge=0.0, le=1.0, description="Razao maxima fora da geometria.")


class CoordToGeohashRunResponse(BaseModel):
    run_id: str
    geohash_count: int
    geohashes: list[str]
    stats_by_length: dict[int, int]
    rings_count: int
