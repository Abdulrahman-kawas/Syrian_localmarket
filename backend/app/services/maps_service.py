"""Google Maps proxy — the API key stays server-side and never reaches clients."""

from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import bad_request
from app.core.logging import get_logger
from app.db.postgis import haversine_km
from app.schemas.common import LatLng

logger = get_logger("app.maps")

_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


def _google_maps_link(origin: LatLng, destination: LatLng) -> str:
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin.latitude},{origin.longitude}"
        f"&destination={destination.latitude},{destination.longitude}"
    )


def directions(origin: LatLng, destination: LatLng) -> dict[str, Any]:
    """Return distance/duration/link. Falls back to a straight-line estimate if no key."""
    link = _google_maps_link(origin, destination)

    if not settings.google_maps_api_key:
        km = haversine_km(
            origin.latitude, origin.longitude, destination.latitude, destination.longitude
        )
        return {
            "distance": f"{km:.1f} km",
            "duration": "unknown",
            "directions_url": link,
        }

    try:
        resp = httpx.get(
            _DIRECTIONS_URL,
            params={
                "origin": f"{origin.latitude},{origin.longitude}",
                "destination": f"{destination.latitude},{destination.longitude}",
                "key": settings.google_maps_api_key,
            },
            timeout=8.0,
        )
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPError as exc:
        logger.error("maps_request_failed", exc_info=exc)
        raise bad_request("Unable to fetch directions") from exc

    routes = data.get("routes") or []
    if not routes:
        raise bad_request("No route found")
    leg = routes[0]["legs"][0]
    return {
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "directions_url": link,
    }
