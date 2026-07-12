"""Seller profile router."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_seller, require_role
from app.db.postgis import geometry_to_geojson
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.seller import Seller
from app.models.user import User
from app.schemas.seller import (
    SellerOnboardRequest,
    SellerOut,
    SellerUpdateRequest,
)
from app.services import seller_service

router = APIRouter(prefix="/sellers", tags=["sellers"])


def _to_out(seller: Seller) -> SellerOut:
    # Build explicitly: the raw geo_point is a WKBElement, not a GeoPoint dict.
    return SellerOut(
        id=seller.id,
        type=seller.type,
        shop_name=seller.shop_name,
        category_id=seller.category_id,
        geo_point=geometry_to_geojson(seller.geo_point),  # type: ignore[arg-type]
        plus_code=seller.plus_code,
        location_description=seller.location_description,
        shop_photo_url=seller.shop_photo_url,
        personal_photo_url=seller.personal_photo_url,
        exterior_photos=list(seller.exterior_photos or []),
    )


@router.post("/onboard", response_model=SellerOut, status_code=201)
def onboard(
    payload: SellerOnboardRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.seller)),
) -> SellerOut:
    seller = seller_service.onboard(db, user, payload)
    return _to_out(seller)


@router.get("/me", response_model=SellerOut)
def get_me(seller: Seller = Depends(get_current_seller)) -> SellerOut:
    return _to_out(seller)


@router.put("/me", response_model=SellerOut)
def update_me(
    payload: SellerUpdateRequest,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> SellerOut:
    updated = seller_service.update(db, seller, payload)
    return _to_out(updated)
