"""Shared FastAPI dependencies: authentication and role/authorization guards."""

from __future__ import annotations

import uuid
from collections.abc import Callable

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import forbidden, unauthorized
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.enums import UserRole, VerificationStatus
from app.models.seller import Seller
from app.models.user import User

# auto_error=False so we can raise our own structured 401 envelope.
_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    """Resolve and validate the caller's JWT into a User row."""
    if credentials is None or not credentials.credentials:
        raise unauthorized()
    claims = decode_access_token(credentials.credentials)
    if not claims or "sub" not in claims:
        raise unauthorized("Invalid or expired token")
    try:
        user_id = uuid.UUID(str(claims["sub"]))
    except ValueError as exc:
        raise unauthorized("Invalid token subject") from exc

    user = db.get(User, user_id)
    if user is None:
        raise unauthorized("User not found")
    if user.is_suspended:
        raise forbidden("Account suspended")
    return user


def get_verified_user(user: User = Depends(get_current_user)) -> User:
    """Require an account that has completed verification."""
    if user.verification_status != VerificationStatus.verified:
        raise forbidden("Account not verified")
    return user


def require_role(*roles: UserRole) -> Callable[[User], User]:
    """Dependency factory enforcing that the caller has one of ``roles``."""

    def _dep(user: User = Depends(get_verified_user)) -> User:
        if user.role not in roles:
            raise forbidden("Insufficient permissions")
        return user

    return _dep


def get_current_seller(
    user: User = Depends(get_verified_user),
    db: Session = Depends(get_db),
) -> Seller:
    """Require a seller account that has completed onboarding."""
    if user.role != UserRole.seller:
        raise forbidden("Seller account required")
    seller = db.query(Seller).filter(Seller.user_id == user.id).one_or_none()
    if seller is None:
        raise forbidden("Complete seller onboarding first")
    return seller


require_admin = require_role(UserRole.admin)
