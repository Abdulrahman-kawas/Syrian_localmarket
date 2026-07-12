"""QR router: get code (seller), scan (consumer), confirm (seller)."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_seller, require_role
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.seller import Seller
from app.models.user import User
from app.schemas.interactions import (
    QRCodeOut,
    QRConfirmRequest,
    QRConfirmResponse,
    QRScanRequest,
    QRScanResponse,
)
from app.services import listing_service, qr_service

# Two path families share this router: /products/{id}/qr and /qr/*
router = APIRouter(tags=["qr"])


@router.get("/products/{product_id}/qr", response_model=QRCodeOut)
def get_qr(
    product_id: uuid.UUID,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> QRCodeOut:
    product = listing_service.get_required(db, product_id)
    qr = qr_service.get_or_create_qr(db, seller, product)
    return QRCodeOut(code=qr.code, image_url=qr.image_url)


@router.post("/qr/scan", response_model=QRScanResponse)
def scan(
    payload: QRScanRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.consumer)),
) -> QRScanResponse:
    txn = qr_service.scan(db, user.id, payload.code)
    return QRScanResponse(transaction_id=txn.id, status=txn.status.value)


@router.post("/qr/confirm/{transaction_id}", response_model=QRConfirmResponse)
def confirm(
    transaction_id: uuid.UUID,
    payload: QRConfirmRequest,
    db: Session = Depends(get_db),
    seller: Seller = Depends(get_current_seller),
) -> QRConfirmResponse:
    txn, proof = qr_service.confirm(db, seller, transaction_id, payload.quantity)
    return QRConfirmResponse(transaction_id=txn.id, status=txn.status.value, proof_record=proof)
