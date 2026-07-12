"""Maps router: nearby sellers and directions (Google proxied server-side)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.postgis import geometry_to_geojson
from app.db.session import get_db
from app.schemas.interactions import DirectionsRequest, DirectionsResponse
from app.services import maps_service
from app.services.search_service import nearby_sellers

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("/nearby")
def nearby(
    db: Session = Depends(get_db),
    lat: float = Query(ge=-90, le=90),
    lng: float = Query(ge=-180, le=180),
    radius: float = Query(default=5.0, gt=0, le=100),
) -> dict[str, Any]:
    sellers = nearby_sellers(db, lat, lng, radius)
    return {
        "sellers": [
            {
                "id": str(s.id),
                "shop_name": s.shop_name,
                "type": s.type.value,
                "geo_point": geometry_to_geojson(s.geo_point),
                "category": (
                    {"name_ar": s.category.name_ar, "name_en": s.category.name_en}
                    if s.category
                    else None
                ),
            }
            for s in sellers
        ]
    }


@router.post("/directions", response_model=DirectionsResponse)
def directions(payload: DirectionsRequest) -> DirectionsResponse:
    result = maps_service.directions(payload.origin, payload.destination)
    return DirectionsResponse(**result)
