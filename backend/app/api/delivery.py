"""Delivery request router (no payment)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_verified_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.interactions import (
    DeliveryCreate,
    DeliveryOut,
    DeliveryStatusUpdate,
)
from app.services import delivery_service

router = APIRouter(prefix="/delivery", tags=["delivery"])


@router.post("", response_model=DeliveryOut, status_code=status.HTTP_201_CREATED)
def create_delivery(
    payload: DeliveryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> DeliveryOut:
    req = delivery_service.create(db, user, payload)
    return DeliveryOut.model_validate(req)


@router.get("", response_model=list[DeliveryOut])
def list_delivery(
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> list[DeliveryOut]:
    rows = delivery_service.list_for_user(db, user)
    return [DeliveryOut.model_validate(r) for r in rows]


@router.put("/{request_id}/status", response_model=DeliveryOut)
def update_status(
    request_id: uuid.UUID,
    payload: DeliveryStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> DeliveryOut:
    req = delivery_service.update_status(db, user, request_id, payload.status)
    return DeliveryOut.model_validate(req)
