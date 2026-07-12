"""Unit tests for password hashing and JWT handling (no DB required)."""

from __future__ import annotations

import uuid

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_roundtrip() -> None:
    h = hash_password("s3cret-pass")
    assert h != "s3cret-pass"
    assert verify_password("s3cret-pass", h)
    assert not verify_password("wrong", h)


def test_verify_password_bad_hash_is_false() -> None:
    assert verify_password("x", "not-a-real-hash") is False


def test_jwt_roundtrip() -> None:
    uid = uuid.uuid4()
    token = create_access_token(uid, "seller")
    claims = decode_access_token(token)
    assert claims is not None
    assert claims["sub"] == str(uid)
    assert claims["role"] == "seller"


def test_jwt_tampered_is_rejected() -> None:
    token = create_access_token(uuid.uuid4(), "consumer")
    assert decode_access_token(token + "tamper") is None


def test_jwt_expired_is_rejected() -> None:
    token = create_access_token(uuid.uuid4(), "consumer", expires_minutes=-1)
    assert decode_access_token(token) is None
