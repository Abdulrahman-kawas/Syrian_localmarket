"""Unit tests for schema validation, incl. food-safety and pricing rules."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.enums import ExpiryClass, ProductType, UserRole, VerificationMethod
from app.schemas.auth import SignupRequest
from app.schemas.product import ProductCreate


def test_signup_email_required_for_email_method() -> None:
    with pytest.raises(ValidationError):
        SignupRequest(
            phone="+963912345678",
            password="password123",
            verification_method=VerificationMethod.email,
        )


def test_signup_rejects_admin_role() -> None:
    with pytest.raises(ValidationError):
        SignupRequest(
            email="a@b.com",
            phone="+963912345678",
            password="password123",
            role=UserRole.admin,
        )


def test_signup_rejects_bad_phone() -> None:
    with pytest.raises(ValidationError):
        SignupRequest(email="a@b.com", phone="not-a-phone", password="password123")


def test_product_discount_cannot_exceed_original() -> None:
    with pytest.raises(ValidationError):
        ProductCreate(
            title="x",
            type=ProductType.market_discount,
            original_price=Decimal("100"),
            discounted_price=Decimal("150"),
            quantity=1,
        )


def test_use_by_past_date_rejected() -> None:
    with pytest.raises(ValidationError):
        ProductCreate(
            title="milk",
            type=ProductType.near_expiry,
            original_price=Decimal("100"),
            discounted_price=Decimal("50"),
            quantity=1,
            expiry_class=ExpiryClass.use_by,
            expiry_date=date.today() - timedelta(days=1),
        )


def test_best_before_past_date_allowed() -> None:
    # best_before items past date MAY be listed (SECURITY.md §8).
    p = ProductCreate(
        title="bread",
        type=ProductType.near_expiry,
        original_price=Decimal("100"),
        discounted_price=Decimal("50"),
        quantity=1,
        expiry_class=ExpiryClass.best_before,
        expiry_date=date.today() - timedelta(days=1),
    )
    assert p.discounted_price == Decimal("50")
