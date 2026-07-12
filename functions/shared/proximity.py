"""Proximity notification logic.

Finds newly-listed discount/near-expiry deals and pushes a notification to the
consumers whose last-known location is within range of the deal's seller. Falls
back to broadcasting only when no consumer has shared a location yet.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.db.postgis import geometry_to_coordinates, within_radius_expr
from app.models.device import DeviceRegistration
from app.models.enums import ProductStatus, ProductType, UserRole
from app.models.product import Product
from app.models.seller import Seller
from app.models.user import User
from app.services import notification_service

_DEAL_TYPES = (ProductType.near_expiry, ProductType.market_discount)


def find_recent_deals(db: Session, since: datetime) -> list[Product]:
    """Active discount/near-expiry products created since ``since``."""
    stmt = (
        select(Product)
        .options(joinedload(Product.seller))
        .where(
            Product.status == ProductStatus.active,
            Product.type.in_(_DEAL_TYPES),
            Product.created_at >= since,
        )
    )
    return list(db.scalars(stmt).unique().all())


def deals_near(db: Session, lat: float, lng: float, radius_km: float) -> list[Product]:
    """Active deals whose seller is within ``radius_km`` of a point (geo primitive)."""
    stmt = (
        select(Product)
        .join(Seller, Product.seller_id == Seller.id)
        .where(
            Product.status == ProductStatus.active,
            Product.type.in_(_DEAL_TYPES),
            within_radius_expr(Seller.geo_point, lat, lng, radius_km),
        )
    )
    return list(db.scalars(stmt).unique().all())


def tokens_near(db: Session, lat: float, lng: float, radius_km: float) -> list[str]:
    """Push tokens of *consumers* whose last-known location is within radius."""
    stmt = (
        select(DeviceRegistration.token)
        .join(User, User.id == DeviceRegistration.user_id)
        .where(
            User.role == UserRole.consumer,
            User.last_location.is_not(None),
            within_radius_expr(User.last_location, lat, lng, radius_km),
        )
    )
    return list(db.scalars(stmt).all())


def run_proximity(db: Session, window_minutes: int = 15) -> dict[str, int]:
    """Notify nearby consumers about deals listed in the last window."""
    since = datetime.now(UTC) - timedelta(minutes=window_minutes)
    deals = find_recent_deals(db, since)
    if not deals:
        return {"deals": 0, "notifications": 0}

    radius = settings.proximity_radius_km
    notified = 0
    targeted_users = 0
    for product in deals:
        seller = product.seller
        coords = geometry_to_coordinates(seller.geo_point) if seller else None
        if coords is None:
            continue
        lat, lng = coords
        tokens = tokens_near(db, lat, lng, radius)
        if not tokens:
            continue
        targeted_users += len(tokens)
        shop = seller.shop_name if seller else "A nearby shop"
        title = "New deal near you"
        body = f"{shop}: {product.title} at a discount"
        notification_service._dispatch(tokens, title, body, {"product_id": str(product.id)})
        notified += len(tokens)

    return {"deals": len(deals), "notifications": notified, "targeted": targeted_users}
