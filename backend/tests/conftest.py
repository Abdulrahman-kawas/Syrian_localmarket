"""Shared pytest fixtures.

Unit tests (security, schemas) run anywhere. Integration tests require a reachable
PostGIS database (DATABASE_URL); when absent they are skipped, keeping CI green.
"""

from __future__ import annotations

import os

# Disable rate limiting for the test run BEFORE any app module loads settings.
os.environ.setdefault("RATE_LIMIT_ENABLED", "false")

import uuid  # noqa: E402

import pytest  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.db.session import SessionLocal, engine  # noqa: E402

_TABLES = [
    "admin_actions",
    "blocks",
    "device_registrations",
    "subscriptions",
    "messages",
    "conversations",
    "delivery_requests",
    "reviews",
    "complaints",
    "transactions",
    "price_history",
    "product_qr",
    "products",
    "sellers",
    "categories",
    "users",
]


def _db_reachable() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:  # noqa: BLE001 - any connection error means "skip integration"
        return False


DB_AVAILABLE = _db_reachable()

requires_db = pytest.mark.skipif(
    not DB_AVAILABLE, reason="No PostGIS database reachable (set DATABASE_URL)"
)


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def _clean_tables():
    """Truncate all app tables before each integration test for isolation."""
    if not DB_AVAILABLE:
        yield
        return
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE {', '.join(_TABLES)} RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)


def unique_email() -> str:
    return f"user_{uuid.uuid4().hex[:10]}@example.com"


def unique_phone() -> str:
    return "+96393" + uuid.uuid4().int.__str__()[:7]
