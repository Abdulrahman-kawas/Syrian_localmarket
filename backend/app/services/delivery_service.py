"""Delivery request lifecycle (no payment involved)."""

from __future__ import annotations

import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.errors import forbidden, not_found
from app.db.postgis import make_point
from app.models.delivery import DeliveryRequest
from app.models.enums import DeliveryStatus
from app.models.seller import Seller
from app.models.user import User
from app.schemas.interactions import DeliveryCreate
from app.services.moderation_service import sanitize_text


def create(db: Session, consumer: User, payload: DeliveryCreate) -> DeliveryRequest:
    if db.get(Seller, payload.seller_id) is None:
        raise not_found("Seller not found")
    req = DeliveryRequest(
        consumer_id=consumer.id,
        seller_id=payload.seller_id,
        product_id=payload.product_id,
        geo_point=make_point(payload.location.latitude, payload.location.longitude),
        location_description=sanitize_text(payload.location.description),
        status=DeliveryStatus.pending,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


def list_for_user(db: Session, user: User) -> list[DeliveryRequest]:
    """Return delivery requests the user is party to (as consumer or as seller)."""
    seller = db.query(Seller).filter(Seller.user_id == user.id).one_or_none()
    seller_id = seller.id if seller else None
    return (
        db.query(DeliveryRequest)
        .filter(
            or_(
                DeliveryRequest.consumer_id == user.id,
                DeliveryRequest.seller_id == seller_id,
            )
        )
        .order_by(DeliveryRequest.created_at.desc())
        .all()
    )


def update_status(
    db: Session, user: User, request_id: uuid.UUID, status: DeliveryStatus
) -> DeliveryRequest:
    req = db.get(DeliveryRequest, request_id)
    if req is None:
        raise not_found("Delivery request not found")

    seller = db.query(Seller).filter(Seller.user_id == user.id).one_or_none()
    is_consumer = req.consumer_id == user.id
    is_seller = seller is not None and req.seller_id == seller.id
    if not (is_consumer or is_seller):
        raise forbidden("Not authorized for this request")

    # Consumers may only cancel; sellers may accept/complete/cancel.
    if is_consumer and not is_seller and status != DeliveryStatus.cancelled:
        raise forbidden("Consumers can only cancel a request")

    req.status = status
    db.commit()
    db.refresh(req)
    return req
