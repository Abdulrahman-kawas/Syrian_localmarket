"""QR generation, consumer scan, and seller confirm-with-decrement flow."""

from __future__ import annotations

import base64
import io
import secrets
import uuid
from datetime import UTC, datetime

import qrcode
from sqlalchemy.orm import Session

from app.core.errors import bad_request, forbidden, not_found
from app.models.enums import ProductStatus, TransactionStatus
from app.models.product import Product, ProductQR
from app.models.seller import Seller
from app.models.transaction import Transaction
from app.schemas.interactions import ProofRecord
from app.services import listing_service


def _new_code() -> str:
    return secrets.token_urlsafe(16)


def _render_png_data_uri(code: str) -> str:
    """Render the QR as a base64 PNG data URI (works offline without blob storage)."""
    img = qrcode.make(code)
    buf = io.BytesIO()
    # qrcode.make returns a Pillow-backed image at runtime whose save() accepts
    # `format`; the stub models the pure-Python PNG image, which does not.
    img.save(buf, format="PNG")  # type: ignore[call-arg]
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def get_or_create_qr(db: Session, seller: Seller, product: Product) -> ProductQR:
    """Return the product's QR, creating it on first request. Owner-only."""
    if product.seller_id != seller.id:
        raise forbidden("You do not own this product")
    if product.qr is not None:
        return product.qr
    qr = ProductQR(
        product_id=product.id,
        code=_new_code(),
    )
    qr.image_url = _render_png_data_uri(qr.code)
    db.add(qr)
    db.commit()
    db.refresh(qr)
    return qr


def scan(db: Session, consumer_id: uuid.UUID, code: str) -> Transaction:
    """Consumer scans a QR: opens a pending transaction against the product."""
    qr = db.query(ProductQR).filter(ProductQR.code == code).one_or_none()
    if qr is None:
        raise not_found("QR code not recognized")
    product = db.get(Product, qr.product_id)
    if product is None:
        raise not_found("Product not found")
    if product.status != ProductStatus.active or product.quantity <= 0:
        raise bad_request("Product is not available")

    txn = Transaction(
        product_id=product.id,
        seller_id=product.seller_id,
        consumer_id=consumer_id,
        quantity=1,
        status=TransactionStatus.pending,
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def confirm(
    db: Session, seller: Seller, transaction_id: uuid.UUID, quantity: int
) -> tuple[Transaction, ProofRecord]:
    """Seller confirms a scan with the sold quantity; decrements stock atomically."""
    txn = db.get(Transaction, transaction_id)
    if txn is None:
        raise not_found("Transaction not found")
    if txn.seller_id != seller.id:
        raise forbidden("This transaction is not yours")
    if txn.status != TransactionStatus.pending:
        raise bad_request("Transaction already resolved")

    product = db.get(Product, txn.product_id)
    if product is None:
        raise not_found("Product not found")
    if quantity > product.quantity:
        raise bad_request("Requested quantity exceeds available stock")

    listing_service.decrement_stock(db, product, quantity)
    txn.quantity = quantity
    txn.status = TransactionStatus.confirmed
    txn.confirmed_at = datetime.now(UTC)
    db.commit()
    db.refresh(txn)

    proof = ProofRecord(
        buyer=txn.consumer_id,
        seller=txn.seller_id,
        product=txn.product_id,
        quantity=txn.quantity,
        timestamp=txn.confirmed_at or datetime.now(UTC),
    )
    return txn, proof
