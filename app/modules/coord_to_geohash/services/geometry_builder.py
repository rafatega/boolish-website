from __future__ import annotations

from shapely.geometry import GeometryCollection, MultiPolygon, Polygon
from shapely.ops import unary_union

from app.modules.coord_to_geohash.domain.errors import CoordToGeohashValidationError
from app.modules.coord_to_geohash.services.coordinate_parser import Ring


class GeometryBuilder:
    def build_from_rings(self, rings: list[Ring]):
        polygons: list[Polygon | MultiPolygon] = []

        for ring in rings:
            ring_points = ring if ring[0] == ring[-1] else ring + [ring[0]]
            polygon = Polygon(ring_points)

            if not polygon.is_valid:
                polygon = polygon.buffer(0)

            if not polygon.is_empty and polygon.area > 0:
                polygons.append(polygon)

        if not polygons:
            raise CoordToGeohashValidationError(
                "Nao foi possivel construir aneis validos a partir das coordenadas."
            )

        geometry = unary_union(polygons)

        if isinstance(geometry, GeometryCollection):
            polygon_parts = [
                part
                for part in geometry.geoms
                if isinstance(part, (Polygon, MultiPolygon))
            ]
            geometry = unary_union(polygon_parts) if polygon_parts else geometry

        return geometry
