"""Auto-delist logic (SECURITY.md §8): expire past-date use_by items and
mark zero-stock items sold out. Importable + unit-testable."""

from __future__ import annotations

from datetime import date

from sqlalchemy import and_, update
from sqlalchemy.orm import Session

from app.models.enums import ExpiryClass, ProductStatus
from app.models.product import Product


def run_auto_delist(db: Session, today: date | None = None) -> dict[str, int]:
    """Reconcile product statuses. Returns counts of what changed."""
    today = today or date.today()

    expired = db.execute(
        update(Product)
        .where(
            and_(
                Product.status == ProductStatus.active,
                Product.expiry_class == ExpiryClass.use_by,
                Product.expiry_date.is_not(None),
                Product.expiry_date < today,
            )
        )
        .values(status=ProductStatus.expired)
    ).rowcount

    sold_out = db.execute(
        update(Product)
        .where(
            and_(
                Product.status == ProductStatus.active,
                Product.quantity <= 0,
            )
        )
        .values(status=ProductStatus.sold_out)
    ).rowcount

    db.commit()
    return {"expired": int(expired or 0), "sold_out": int(sold_out or 0)}
