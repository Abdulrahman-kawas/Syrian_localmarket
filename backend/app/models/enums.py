"""Enumerations shared across models and schemas."""

from __future__ import annotations

import enum
from typing import Any

from sqlalchemy import Enum as SAEnum


class UserRole(str, enum.Enum):
    consumer = "consumer"
    seller = "seller"
    admin = "admin"


class VerificationMethod(str, enum.Enum):
    email = "email"
    whatsapp = "whatsapp"


class VerificationStatus(str, enum.Enum):
    pending = "pending"
    verified = "verified"
    failed = "failed"


class SellerType(str, enum.Enum):
    shop = "shop"
    factory = "factory"


class ProductType(str, enum.Enum):
    regular = "regular"
    market_discount = "market_discount"
    near_expiry = "near_expiry"


class ExpiryClass(str, enum.Enum):
    best_before = "best_before"
    use_by = "use_by"


class ProductStatus(str, enum.Enum):
    active = "active"
    sold_out = "sold_out"
    expired = "expired"
    hidden = "hidden"


class TransactionStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    expired = "expired"


class ReviewTargetType(str, enum.Enum):
    seller = "seller"
    consumer = "consumer"


class ReviewStatus(str, enum.Enum):
    active = "active"
    hidden = "hidden"
    reported = "reported"


class ComplaintTargetType(str, enum.Enum):
    seller = "seller"
    listing = "listing"
    review = "review"


class ComplaintStatus(str, enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    resolved = "resolved"


class DeliveryStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    completed = "completed"
    cancelled = "cancelled"


class DevicePlatform(str, enum.Enum):
    apns = "apns"
    fcm = "fcm"


class SubscriptionTier(str, enum.Enum):
    consumer = "consumer"
    shop = "shop"
    factory = "factory"


class AdminActionType(str, enum.Enum):
    suspend = "suspend"
    adjust_reputation = "adjust_reputation"
    resolve_complaint = "resolve_complaint"


class AdminTargetType(str, enum.Enum):
    user = "user"
    listing = "listing"
    complaint = "complaint"


def pg_enum(enum_cls: type[enum.Enum], name: str) -> Any:
    """Build a Postgres ENUM that stores the enum *values* (lowercase strings)."""
    return SAEnum(
        enum_cls,
        name=name,
        values_callable=lambda e: [member.value for member in e],
        native_enum=True,
    )
