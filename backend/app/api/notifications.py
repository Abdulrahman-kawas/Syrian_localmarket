"""Notifications router: device registration for push."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_verified_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.interactions import DeviceRegisterRequest, OkResponse
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/register", response_model=OkResponse)
def register(
    payload: DeviceRegisterRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> OkResponse:
    notification_service.register_device(db, user.id, payload.platform, payload.token)
    return OkResponse()
