"""PostGIS helpers for point geometry and distance queries."""

from __future__ import annotations

import math
from typing import Any

from geoalchemy2 import Geography, Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy import func

# SRID 4326 == WGS84 lat/lng, the standard for GPS coordinates.
SRID = 4326

# Column type used by models that store a location.
PointGeometry = Geometry(geometry_type="POINT", srid=SRID, spatial_index=True)


def make_point(latitude: float, longitude: float) -> Any:
    """Build a PostGIS POINT geometry from lat/lng (note PostGIS order is lng, lat)."""
    return func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), SRID)


def geometry_to_coordinates(geom: Any) -> tuple[float, float] | None:
    """Return (latitude, longitude) from a stored geometry value, or None."""
    if geom is None:
        return None
    shape = to_shape(geom)
    # shapely stores x=lng, y=lat
    return (shape.y, shape.x)


def geometry_to_geojson(geom: Any) -> dict[str, Any] | None:
    """Return a GeoJSON Point ({type, coordinates:[lng, lat]}) for API responses."""
    coords = geometry_to_coordinates(geom)
    if coords is None:
        return None
    lat, lng = coords
    return {"type": "Point", "coordinates": [lng, lat]}


def distance_meters_expr(geom_column: Any, latitude: float, longitude: float) -> Any:
    """SQL expression for geodesic distance (metres) between a column and a point."""
    return func.ST_Distance(
        func.ST_Transform(geom_column, 3857),
        func.ST_Transform(make_point(latitude, longitude), 3857),
    )


def within_radius_expr(
    geom_column: Any, latitude: float, longitude: float, radius_km: float
) -> Any:
    """SQL predicate: is the column within `radius_km` of the given point?

    Casts geometries to ``geography`` so ST_DWithin measures true metres on the
    WGS84 spheroid regardless of location.
    """
    return func.ST_DWithin(
        geom_column.cast(Geography),
        make_point(latitude, longitude).cast(Geography),
        radius_km * 1000.0,
    )


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Great-circle distance in km — used by background jobs and offline tests."""
    r = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.asin(math.sqrt(a))
