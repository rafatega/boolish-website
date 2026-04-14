from __future__ import annotations

from app.core.settings import settings
from app.modules.coord_to_geohash.services.coordinate_parser import CoordinateParser, RingDetector
from app.modules.coord_to_geohash.services.geohash_coverage import GeohashCoverageService
from app.modules.coord_to_geohash.services.geometry_builder import GeometryBuilder
from app.modules.coord_to_geohash.services.renderers import GeohashMapRenderer, GeohashSpreadsheetRenderer
from app.modules.coord_to_geohash.services.use_case import CoordToGeohashUseCase
from app.shared.storage.expiring_run_store import ExpiringRunStore

run_store = ExpiringRunStore(ttl=settings.run_ttl)

coord_to_geohash_use_case = CoordToGeohashUseCase(
    coordinate_parser=CoordinateParser(),
    ring_detector=RingDetector(),
    geometry_builder=GeometryBuilder(),
    geohash_coverage_service=GeohashCoverageService(),
    map_renderer=GeohashMapRenderer(),
    spreadsheet_renderer=GeohashSpreadsheetRenderer(),
)
