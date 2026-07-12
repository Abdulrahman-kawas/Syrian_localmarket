"""User model for all roles (consumer, seller, admin), plus Block."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Index, Numeric, String, func, text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, uuid_pk
from app.db.postgis import SRID
from app.models.enums import (
    UserRole,
    VerificationMethod,
    VerificationStatus,
    pg_enum,
)

if TYPE_CHECKING:
    from app.models.seller import Seller


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = uuid_pk()
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    whatsapp: Mapped[str | None] = mapped_column(String(20), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(pg_enum(UserRole, "user_role"), nullable=False)
    verification_method: Mapped[VerificationMethod] = mapped_column(
        pg_enum(VerificationMethod, "verification_method"), nullable=False
    )
    verification_status: Mapped[VerificationStatus] = mapped_column(
        pg_enum(VerificationStatus, "verification_status"),
        nullable=False,
        default=VerificationStatus.pending,
    )
    verification_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_last: Mapped[str | None] = mapped_column(INET, nullable=True)
    reputation_score: Mapped[Decimal] = mapped_column(
        Numeric(3, 2), nullable=False, server_default=text("1.00")
    )
    is_suspended: Mapped[bool] = mapped_column(nullable=False, server_default=text("false"))
    # Last-known consumer location for proximity notifications (opt-in, updated
    # by the app). Index is created explicitly in migration 0002.
    last_location: Mapped[Any | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=SRID, spatial_index=False), nullable=True
    )

    seller: Mapped[Seller | None] = relationship(
        "Seller", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_users_role", "role"),)


class Block(Base):
    __tablename__ = "blocks"

    id: Mapped[uuid.UUID] = uuid_pk()
    blocker_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, index=True)
    blocked_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (Index("ux_blocks_pair", "blocker_id", "blocked_id", unique=True),)
