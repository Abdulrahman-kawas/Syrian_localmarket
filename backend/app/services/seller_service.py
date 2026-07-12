"""Seller onboarding and profile management."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import conflict, not_found
from app.db.postgis import make_point
from app.models.seller import Seller
from app.models.user import User
from app.schemas.seller import SellerOnboardRequest, SellerUpdateRequest
from app.services.moderation_service import sanitize_text


def get_by_user(db: Session, user_id: object) -> Seller | None:
    return db.query(Seller).filter(Seller.user_id == user_id).one_or_none()


def onboard(db: Session, user: User, payload: SellerOnboardRequest) -> Seller:
    """Create the 1:1 seller profile for a seller user."""
    if get_by_user(db, user.id) is not None:
        raise conflict("Seller profile already exists")

    seller = Seller(
        user_id=user.id,
        type=payload.type,
        shop_name=sanitize_text(payload.shop_name) or payload.shop_name,
        category_id=payload.category_id,
        geo_point=make_point(payload.location.latitude, payload.location.longitude),
        plus_code=payload.location.plus_code,
        location_description=sanitize_text(payload.location.description),
        shop_photo_url=payload.shop_photo_url,
        personal_photo_url=payload.personal_photo_url,
        exterior_photos=payload.exterior_photos,
    )
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


def update(db: Session, seller: Seller, payload: SellerUpdateRequest) -> Seller:
    """Patch mutable seller fields (object-level auth enforced by the caller)."""
    if payload.shop_name is not None:
        seller.shop_name = sanitize_text(payload.shop_name) or seller.shop_name
    if payload.category_id is not None:
        seller.category_id = payload.category_id
    if payload.location is not None:
        seller.geo_point = make_point(payload.location.latitude, payload.location.longitude)
        seller.plus_code = payload.location.plus_code
        seller.location_description = sanitize_text(payload.location.description)
    if payload.shop_photo_url is not None:
        seller.shop_photo_url = payload.shop_photo_url
    if payload.personal_photo_url is not None:
        seller.personal_photo_url = payload.personal_photo_url
    if payload.exterior_photos is not None:
        seller.exterior_photos = payload.exterior_photos
    db.commit()
    db.refresh(seller)
    return seller


def get_required(db: Session, seller_id: object) -> Seller:
    seller = db.get(Seller, seller_id)
    if seller is None:
        raise not_found("Seller not found")
    return seller
