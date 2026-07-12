"""Product listing CRUD, stock editing, price-history tracking, auto-delist."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.core.errors import forbidden, not_found
from app.models.enums import ExpiryClass, ProductStatus
from app.models.product import PriceHistory, Product
from app.models.seller import Seller
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.schemas.seller import SellerSummary
from app.services.moderation_service import sanitize_text


def _record_price(db: Session, product: Product, changed_by: uuid.UUID | None) -> None:
    db.add(
        PriceHistory(
            product_id=product.id,
            original_price=product.original_price,
            discounted_price=product.discounted_price,
            changed_by=changed_by,
        )
    )


def create(db: Session, seller: Seller, payload: ProductCreate) -> Product:
    product = Product(
        seller_id=seller.id,
        type=payload.type,
        title=sanitize_text(payload.title) or payload.title,
        description=sanitize_text(payload.description),
        images=payload.images,
        original_price=payload.original_price,
        discounted_price=payload.discounted_price,
        currency=payload.currency,
        expiry_date=payload.expiry_date,
        expiry_class=payload.expiry_class,
        quantity=payload.quantity,
        status=ProductStatus.active if payload.quantity > 0 else ProductStatus.sold_out,
    )
    db.add(product)
    db.flush()
    _record_price(db, product, seller.user_id)
    db.commit()
    db.refresh(product)
    return product


def get_required(db: Session, product_id: uuid.UUID) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise not_found("Product not found")
    return product


def _assert_owner(product: Product, seller: Seller) -> None:
    """Object-level authorization: a seller may only touch their own products."""
    if product.seller_id != seller.id:
        raise forbidden("You do not own this product")


def update(db: Session, seller: Seller, product: Product, payload: ProductUpdate) -> Product:
    _assert_owner(product, seller)
    price_changed = False

    data = payload.model_dump(exclude_unset=True)
    if "title" in data:
        product.title = sanitize_text(data["title"]) or product.title
    if "description" in data:
        product.description = sanitize_text(data["description"])
    if "type" in data:
        product.type = data["type"]
    if "images" in data:
        product.images = data["images"]
    if "expiry_date" in data:
        product.expiry_date = data["expiry_date"]
    if "expiry_class" in data:
        product.expiry_class = data["expiry_class"]
    if "original_price" in data:
        product.original_price = data["original_price"]
        price_changed = True
    if "discounted_price" in data:
        product.discounted_price = data["discounted_price"]
        price_changed = True
    if "quantity" in data:
        product.quantity = data["quantity"]
    if "status" in data:
        product.status = data["status"]

    if product.discounted_price > product.original_price:
        raise forbidden("discounted_price cannot exceed original_price")
    _enforce_food_safety(product)

    if price_changed:
        _record_price(db, product, seller.user_id)
    _reconcile_status(product)
    db.commit()
    db.refresh(product)
    return product


def set_quantity(db: Session, seller: Seller, product: Product, quantity: int) -> Product:
    _assert_owner(product, seller)
    product.quantity = quantity
    _reconcile_status(product)
    db.commit()
    db.refresh(product)
    return product


def delete(db: Session, seller: Seller, product: Product) -> None:
    _assert_owner(product, seller)
    db.delete(product)
    db.commit()


def _enforce_food_safety(product: Product) -> None:
    if (
        product.expiry_class == ExpiryClass.use_by
        and product.expiry_date is not None
        and product.expiry_date < date.today()
    ):
        raise forbidden("use_by items past their expiry date cannot be listed")


def _reconcile_status(product: Product) -> None:
    """Auto-delist rules: 0 stock -> sold_out; past use_by/expiry -> expired."""
    if product.status == ProductStatus.hidden:
        return
    if product.quantity <= 0:
        product.status = ProductStatus.sold_out
    elif (
        product.expiry_date is not None
        and product.expiry_date < date.today()
        and product.expiry_class == ExpiryClass.use_by
    ):
        product.status = ProductStatus.expired
    else:
        product.status = ProductStatus.active


def decrement_stock(db: Session, product: Product, amount: int) -> None:
    """Reduce stock after a confirmed sale and auto-delist if depleted."""
    product.quantity = max(0, product.quantity - amount)
    _reconcile_status(product)
    db.flush()


def to_out(product: Product, *, include_phone: bool = False) -> ProductOut:
    """Serialize a product, attaching a compact seller summary."""
    seller = product.seller
    summary: SellerSummary | None = None
    if seller is not None:
        summary = SellerSummary(
            id=seller.id,
            user_id=seller.user_id,
            shop_name=seller.shop_name,
            type=seller.type,
            phone=seller.user.phone if include_phone and seller.user else None,
        )
    out = ProductOut.model_validate(product)
    out.seller = summary
    return out
