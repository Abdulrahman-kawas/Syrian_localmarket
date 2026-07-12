"""Unified search router (Arabic-aware ILIKE + geo + filters)."""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.enums import ProductType, SellerType
from app.services import listing_service
from app.services.search_service import ProductFilters, search_products

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, max_length=200),
    type: ProductType | None = None,
    seller_type: SellerType | None = None,
    category_id: uuid.UUID | None = None,
    lat: float | None = Query(default=None, ge=-90, le=90),
    lng: float | None = Query(default=None, ge=-180, le=180),
    radius: float | None = Query(default=None, gt=0, le=100),
    min_discount: float | None = Query(default=None, ge=0, le=100),
    max_price: Decimal | None = Query(default=None, ge=0),
    sort: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    filters = ProductFilters(
        q=q,
        type=type,
        seller_type=seller_type,
        category_id=category_id,
        lat=lat,
        lng=lng,
        radius=radius,
        min_discount=min_discount,
        max_price=max_price,
        sort=sort,
    )
    rows, total = search_products(db, filters, page, per_page)
    applied = {
        k: v
        for k, v in {
            "q": q,
            "type": type.value if type else None,
            "seller_type": seller_type.value if seller_type else None,
            "lat": lat,
            "lng": lng,
            "radius": radius,
        }.items()
        if v is not None
    }
    return {
        "items": [listing_service.to_out(p).model_dump(mode="json") for p in rows],
        "total": total,
        "page": page,
        "per_page": per_page,
        "filters_applied": applied,
    }
