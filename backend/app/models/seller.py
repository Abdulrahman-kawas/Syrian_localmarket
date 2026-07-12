"""Seller profile (1:1 with a seller user)."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, uuid_pk
from app.db.postgis import PointGeometry
from app.models.enums import SellerType, pg_enum

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.product import Product
    from app.models.user import User


class Seller(Base, TimestampMixin):
    __tablename__ = "sellers"

    id: Mapped[uuid.UUID] = uuid_pk()
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    type: Mapped[SellerType] = mapped_column(pg_enum(SellerType, "seller_type"), nullable=False)
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True, index=True
    )
    shop_name: Mapped[str] = mapped_column(String(100), nullable=False)
    shop_photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    personal_photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    geo_point: Mapped[Any] = mapped_column(PointGeometry, nullable=False)
    plus_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    location_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    exterior_photos: Mapped[list[str]] = mapped_column(JSONB, nullable=False, server_default="[]")

    user: Mapped[User] = relationship("User", back_populates="seller")
    category: Mapped[Category | None] = relationship("Category")
    products: Mapped[list[Product]] = relationship(
        "Product", back_populates="seller", cascade="all, delete-orphan"
    )
