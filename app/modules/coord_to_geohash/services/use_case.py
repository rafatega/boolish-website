from __future__ import annotations

from collections import Counter

from app.modules.coord_to_geohash.domain.models import CoordToGeohashInput, CoordToGeohashOutput
from app.modules.coord_to_geohash.services.coordinate_parser import CoordinateParser, RingDetector
from app.modules.coord_to_geohash.services.geohash_coverage import GeohashCoverageService
from app.modules.coord_to_geohash.services.geometry_builder import GeometryBuilder
from app.modules.coord_to_geohash.services.renderers import GeohashMapRenderer, GeohashSpreadsheetRenderer


class CoordToGeohashUseCase:
    def __init__(
        self,
        coordinate_parser: CoordinateParser,
        ring_detector: RingDetector,
        geometry_builder: GeometryBuilder,
        geohash_coverage_service: GeohashCoverageService,
        map_renderer: GeohashMapRenderer,
        spreadsheet_renderer: GeohashSpreadsheetRenderer,
    ) -> None:
        self._coordinate_parser = coordinate_parser
        self._ring_detector = ring_detector
        self._geometry_builder = geometry_builder
        self._geohash_coverage_service = geohash_coverage_service
        self._map_renderer = map_renderer
        self._spreadsheet_renderer = spreadsheet_renderer

    def execute(self, command: CoordToGeohashInput) -> CoordToGeohashOutput:
        points = self._coordinate_parser.parse(command.raw_coords)
        rings = self._ring_detector.detect(points)
        geometry = self._geometry_builder.build_from_rings(rings)

        geohashes = sorted(
            self._geohash_coverage_service.calculate(
                geometry=geometry,
                target_precision=command.target_precision,
                max_outside=command.max_outside,
            )
        )

        stats_by_length = dict(sorted(Counter(len(gh) for gh in geohashes).items()))
        map_html = self._map_renderer.render(geometry=geometry, geohashes=geohashes)
        excel_bytes = self._spreadsheet_renderer.render(geohashes=geohashes)

        return CoordToGeohashOutput(
            geohashes=geohashes,
            geohash_count=len(geohashes),
            rings_count=len(rings),
            stats_by_length=stats_by_length,
            map_html=map_html,
            excel_bytes=excel_bytes,
        )
