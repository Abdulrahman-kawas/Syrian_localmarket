"""Integration tests for the Azure Functions timer job logic."""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

# The job logic lives in the sibling `functions/` project; add it to the path.
_FUNCTIONS_DIR = Path(__file__).resolve().parents[2] / "functions"
if str(_FUNCTIONS_DIR) not in sys.path:
    sys.path.insert(0, str(_FUNCTIONS_DIR))

from app.core.security import hash_password  # noqa: E402
from app.db.postgis import make_point  # noqa: E402
from app.models.device import DeviceRegistration  # noqa: E402
from app.models.enums import (  # noqa: E402
    DevicePlatform,  # noqa: E402
    ExpiryClass,
    ProductStatus,
    ProductType,
    SellerType,
    UserRole,
    VerificationMethod,
    VerificationStatus,
)
from app.models.product import Product  # noqa: E402
from app.models.seller import Seller  # noqa: E402
from app.models.user import User  # noqa: E402
from tests.conftest import requires_db, unique_email, unique_phone  # noqa: E402

pytestmark = requires_db


def _consumer_with_location(db, lat: float, lng: float, token: str) -> User:
    """A verified consumer with a last-known location and one device token."""
    user = User(
        email=unique_email(),
        phone=unique_phone(),
        password_hash=hash_password("password123"),
        role=UserRole.consumer,
        verification_method=VerificationMethod.email,
        verification_status=VerificationStatus.verified,
        last_location=make_point(lat, lng),
    )
    db.add(user)
    db.flush()
    db.add(DeviceRegistration(user_id=user.id, platform=DevicePlatform.fcm, token=token))
    db.flush()
    return user


def _seller(db) -> Seller:
    user = User(
        email="jobseller@example.com",
        phone="+963900001111",
        password_hash=hash_password("password123"),
        role=UserRole.seller,
        verification_method=VerificationMethod.email,
        verification_status=VerificationStatus.verified,
    )
    db.add(user)
    db.flush()
    seller = Seller(
        user_id=user.id, type=SellerType.shop, shop_name="Jobs Shop",
        geo_point=make_point(33.5, 36.3),
    )
    db.add(seller)
    db.flush()
    return seller


def test_auto_delist_expires_and_sells_out(db) -> None:
    from shared.delist import run_auto_delist

    seller = _seller(db)
    expired = Product(
        seller_id=seller.id,
        type=ProductType.near_expiry,
        title="old",
        original_price=10,
        discounted_price=5,
        quantity=3,
        expiry_class=ExpiryClass.use_by,
        expiry_date=date.today() - timedelta(days=2),
        status=ProductStatus.active,
    )
    zero = Product(
        seller_id=seller.id,
        type=ProductType.regular,
        title="empty",
        original_price=10,
        discounted_price=5,
        quantity=0,
        status=ProductStatus.active,
    )
    healthy = Product(
        seller_id=seller.id,
        type=ProductType.regular,
        title="ok",
        original_price=10,
        discounted_price=5,
        quantity=9,
        status=ProductStatus.active,
    )
    db.add_all([expired, zero, healthy])
    db.commit()

    result = run_auto_delist(db)
    assert result == {"expired": 1, "sold_out": 1}

    for p in (expired, zero, healthy):
        db.refresh(p)
    assert expired.status == ProductStatus.expired
    assert zero.status == ProductStatus.sold_out
    assert healthy.status == ProductStatus.active


def test_proximity_deals_near(db) -> None:
    from shared.proximity import deals_near

    seller = _seller(db)
    db.add(
        Product(
            seller_id=seller.id,
            type=ProductType.near_expiry,
            title="deal",
            original_price=10,
            discounted_price=5,
            quantity=1,
            status=ProductStatus.active,
        )
    )
    db.commit()

    # Within 5km of the seller -> found; far away -> not found.
    assert len(deals_near(db, 33.5, 36.3, 5)) == 1
    assert len(deals_near(db, 40.0, 40.0, 5)) == 0


def test_proximity_targets_only_nearby_consumers(db) -> None:
    from shared.proximity import run_proximity, tokens_near

    seller = _seller(db)  # located at 33.5, 36.3
    db.add(
        Product(
            seller_id=seller.id,
            type=ProductType.near_expiry,
            title="fresh deal",
            original_price=10,
            discounted_price=5,
            quantity=2,
            status=ProductStatus.active,
        )
    )
    # One consumer next door, one in another city.
    _consumer_with_location(db, 33.5, 36.3, token="near-token")
    _consumer_with_location(db, 40.0, 40.0, token="far-token")
    db.commit()

    near_tokens = tokens_near(db, 33.5, 36.3, radius_km=5)
    assert near_tokens == ["near-token"]

    result = run_proximity(db)
    # The recent deal targets exactly the one nearby consumer's device.
    assert result["deals"] == 1
    assert result["notifications"] == 1
    assert result["targeted"] == 1
