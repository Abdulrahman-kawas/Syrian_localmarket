"""Auth API router: signup, verify, login."""

from __future__ import annotations

import ipaddress

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.rate_limit import auth_rate_limit
from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    SignupResponse,
    TokenResponse,
    UserPublic,
    VerifyRequest,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(auth_rate_limit)])


def _client_ip(request: Request) -> str | None:
    fwd = request.headers.get("x-forwarded-for")
    candidate = (
        fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else None)
    )
    if not candidate:
        return None
    try:
        # Only persist genuine IPs into the INET column (weak anti-fraud signal).
        ipaddress.ip_address(candidate)
    except ValueError:
        return None
    return candidate


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(
    payload: SignupRequest, request: Request, db: Session = Depends(get_db)
) -> SignupResponse:
    user = auth_service.signup(db, payload, client_ip=_client_ip(request))
    return SignupResponse.model_validate(user)


@router.post("/verify", response_model=TokenResponse)
def verify(payload: VerifyRequest, db: Session = Depends(get_db)) -> TokenResponse:
    token, user = auth_service.verify(db, payload)
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    token, user = auth_service.login(db, payload, client_ip=_client_ip(request))
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))
