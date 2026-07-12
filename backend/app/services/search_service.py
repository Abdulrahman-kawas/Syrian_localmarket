"""Geospatial + filtered product search and nearby-seller lookup."""

from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any

from sqlalchemy import Select, and_, or_, select
from sqlalchemy.orm import Session, joinedload

from app.db.postgis import distance_meters_expr, within_radius_expr
from app.models.enums import ProductStatus, ProductType, SellerType
from app.models.product import Product
from app.models.seller import Seller


class ProductFilters:
    """Normalised query filters for product search."""

    def __init__(
        self,
        q: str | None = None,
        type: ProductType | None = None,
        seller_type: SellerType | None = None,
        category_id: uuid.UUID | None = None,
        lat: float | None = None,
        lng: float | None = None,
        radius: float | None = None,
        min_discount: float | None = None,
        max_price: Decimal | None = None,
        sort: str | None = None,
    ) -> None:
        self.q = q
        self.type = type
        self.seller_type = seller_type
        self.category_id = category_id
        self.lat = lat
        self.lng = lng
        self.radius = radius
        self.min_discount = min_discount
        self.max_price = max_price
        self.sort = sort

    @property
    def has_geo(self) -> bool:
        return self.lat is not None and self.lng is not None


def build_query(filters: ProductFilters) -> Select[tuple[Product]]:
    """Compose a SELECT over active products honouring every provided filter."""
    stmt: Select[tuple[Product]] = (
        select(Product)
        .join(Seller, Product.seller_id == Seller.id)
        .options(joinedload(Product.seller).joinedload(Seller.user))
        .where(Product.status == ProductStatus.active)
    )

    if filters.q:
        pattern = f"%{filters.q.strip()}%"
        stmt = stmt.where(or_(Product.title.ilike(pattern), Product.description.ilike(pattern)))
    if filters.type is not None:
        stmt = stmt.where(Product.type == filters.type)
    if filters.seller_type is not None:
        stmt = stmt.where(Seller.type == filters.seller_type)
    if filters.category_id is not None:
        stmt = stmt.where(Seller.category_id == filters.category_id)
    if filters.max_price is not None:
        stmt = stmt.where(Product.discounted_price <= filters.max_price)
    if filters.min_discount is not None:
        # discount% = (original - discounted) / original * 100
        stmt = stmt.where(
            and_(
                Product.original_price > 0,
                (Product.original_price - Product.discounted_price) * 100.0 / Product.original_price
                >= filters.min_discount,
            )
        )
    if filters.lat is not None and filters.lng is not None and filters.radius:
        stmt = stmt.where(
            within_radius_expr(Seller.geo_point, filters.lat, filters.lng, filters.radius)
        )

    stmt = _apply_sort(stmt, filters)
    return stmt


def _apply_sort(stmt: Select[tuple[Product]], filters: ProductFilters) -> Select[tuple[Product]]:
    sort = filters.sort
    if sort == "price_asc":
        return stmt.order_by(Product.discounted_price.asc())
    if sort == "price_desc":
        return stmt.order_by(Product.discounted_price.desc())
    if sort == "expiry_asc":
        return stmt.order_by(Product.expiry_date.asc().nulls_last())
    if sort == "nearby" and filters.lat is not None and filters.lng is not None:
        return stmt.order_by(distance_meters_expr(Seller.geo_point, filters.lat, filters.lng).asc())
    return stmt.order_by(Product.created_at.desc())


def search_products(
    db: Session, filters: ProductFilters, page: int, per_page: int
) -> tuple[list[Product], int]:
    """Return (page_of_products, total_count)."""
    stmt = build_query(filters)
    total = db.scalar(select(count_star()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.limit(per_page).offset((page - 1) * per_page)).unique().all()
    return list(rows), int(total)


def nearby_sellers(db: Session, lat: float, lng: float, radius_km: float) -> list[Seller]:
    stmt = (
        select(Seller)
        .options(joinedload(Seller.category))
        .where(within_radius_expr(Seller.geo_point, lat, lng, radius_km))
        .order_by(distance_meters_expr(Seller.geo_point, lat, lng).asc())
        .limit(200)
    )
    return list(db.scalars(stmt).unique().all())


def count_star() -> Any:
    """Tiny helper returning a SQL COUNT(*) function element."""
    from sqlalchemy import func

    return func.count()
