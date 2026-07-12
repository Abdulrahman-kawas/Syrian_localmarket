"""Product listing router: CRUD, filtering, stock editing."""

from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_seller
from app.db.session import get_db
from app.models.enums import ProductType, SellerType
from app.models.seller import Seller
from app.schemas.common import Page
from app.schemas.product import (
    ProductCreate,
    ProductOut,
    ProductUpdate,
    QuantityUpdate,
)
from app.services import listing_service
from app.services.search_service import ProductFilters, search_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=Page[ProductOut])
def list_products(
    db: Session = Depends(get_db),
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
) -> Page[ProductOut]:
    filters = ProductFilters(
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
    return Page[ProductOut](
        items=[listing_service.to_out(p) for p in rows],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> ProductOut:
    product = listing_service.create(db, seller, payload)
    return listing_service.to_out(product, include_phone=True)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)) -> ProductOut:
    product = listing_service.get_required(db, product_id)
    return listing_service.to_out(product, include_phone=True)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: uuid.UUID,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> ProductOut:
    product = listing_service.get_required(db, product_id)
    updated = listing_service.update(db, seller, product, payload)
    return listing_service.to_out(updated, include_phone=True)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> None:
    product = listing_service.get_required(db, product_id)
    listing_service.delete(db, seller, product)


@router.put("/{product_id}/quantity", response_model=ProductOut)
def update_quantity(
    product_id: uuid.UUID,
    payload: QuantityUpdate,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> ProductOut:
    product = listing_service.get_required(db, product_id)
    updated = listing_service.set_quantity(db, seller, product, payload.quantity)
    return listing_service.to_out(updated, include_phone=True)
