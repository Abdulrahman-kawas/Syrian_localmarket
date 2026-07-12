"""Authentication service: signup, verification, login.

Security notes:
- Passwords are bcrypt-hashed; plaintext is never stored or logged.
- Verification uses email OR WhatsApp codes (no SMS OTP — unreliable in Syria).
- Login and verification failures return generic messages to avoid user enumeration.
"""

from __future__ import annotations

import secrets

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.errors import conflict, unauthorized
from app.core.logging import get_logger
from app.core.security import create_access_token, hash_password, verify_password
from app.models.enums import UserRole, VerificationMethod, VerificationStatus
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, VerifyRequest
from app.services import messaging_service

logger = get_logger("app.auth")


def _generate_code() -> str:
    """Cryptographically-random 6-digit verification code."""
    return f"{secrets.randbelow(1_000_000):06d}"


def signup(db: Session, payload: SignupRequest, client_ip: str | None = None) -> User:
    """Create a pending user and issue a verification code."""
    existing = (
        db.query(User).filter(or_(User.email == payload.email, User.phone == payload.phone)).first()
    )
    if existing is not None:
        # Generic conflict — do not reveal which field collided (anti-enumeration).
        raise conflict("Could not create account with the provided details")

    code = _generate_code()
    user = User(
        email=payload.email,
        phone=payload.phone,
        whatsapp=payload.whatsapp,
        password_hash=hash_password(payload.password),
        role=payload.role,
        verification_method=payload.verification_method,
        verification_status=VerificationStatus.pending,
        verification_code=code,
        ip_last=client_ip,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    _deliver_code(user, code)
    return user


def _deliver_code(user: User, code: str) -> None:
    """Send the verification code via ACS email/WhatsApp (dev falls back to a log).

    The code value is never logged.
    """
    channel = "email" if user.verification_method == VerificationMethod.email else "whatsapp"
    logger.info(
        "verification_code_issued",
        extra={"extra_fields": {"user_id": str(user.id), "channel": channel}},
    )
    messaging_service.send_verification_code(
        method=user.verification_method.value,
        email=user.email,
        phone=user.phone,
        code=code,
    )


def verify(db: Session, payload: VerifyRequest) -> tuple[str, User]:
    """Verify a code and return (access_token, user)."""
    query = db.query(User)
    if payload.email:
        query = query.filter(User.email == payload.email)
    else:
        query = query.filter(User.phone == payload.phone)
    user = query.first()

    if user is None or user.verification_code is None:
        raise unauthorized("Invalid verification details")
    if not secrets.compare_digest(user.verification_code, payload.code):
        raise unauthorized("Invalid verification details")

    user.verification_status = VerificationStatus.verified
    user.verification_code = None
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, user.role.value)
    return token, user


def login(db: Session, payload: LoginRequest, client_ip: str | None = None) -> tuple[str, User]:
    """Authenticate by email/phone + password. Generic errors prevent enumeration."""
    query = db.query(User)
    if payload.email:
        query = query.filter(User.email == payload.email)
    else:
        query = query.filter(User.phone == payload.phone)
    user = query.first()

    # Always run a hash comparison to keep timing uniform whether or not the
    # user exists (mitigates account-enumeration via response timing).
    dummy_hash = "$2b$12$" + "x" * 53
    if user is None:
        verify_password(payload.password, dummy_hash)
        raise unauthorized("Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise unauthorized("Invalid credentials")

    if user.verification_status != VerificationStatus.verified:
        raise unauthorized("Account not verified")
    if user.is_suspended:
        raise unauthorized("Invalid credentials")

    if client_ip:
        user.ip_last = client_ip
        db.commit()

    token = create_access_token(user.id, user.role.value)
    return token, user


def bootstrap_admin(db: Session, email: str, phone: str, password: str) -> User:
    """Idempotently create a verified admin (used by seed scripts, never via API)."""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    admin = User(
        email=email,
        phone=phone,
        password_hash=hash_password(password),
        role=UserRole.admin,
        verification_method=VerificationMethod.email,
        verification_status=VerificationStatus.verified,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
