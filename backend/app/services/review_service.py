"""Ratings & reviews with reputation recomputation."""

from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import bad_request, not_found
from app.models.enums import ReviewStatus
from app.models.review import Review
from app.models.user import User
from app.schemas.interactions import ReviewCreate
from app.services.moderation_service import sanitize_text


def create(db: Session, author: User, payload: ReviewCreate) -> Review:
    if payload.target_id == author.id:
        raise bad_request("You cannot review yourself")
    target = db.get(User, payload.target_id)
    if target is None:
        raise not_found("Target user not found")

    review = Review(
        author_id=author.id,
        target_id=payload.target_id,
        target_type=payload.target_type,
        rating=payload.rating,
        text=sanitize_text(payload.text),
        status=ReviewStatus.active,
    )
    db.add(review)
    db.flush()
    _recompute_reputation(db, payload.target_id)
    db.commit()
    db.refresh(review)
    return review


def list_for_target(db: Session, target_id: uuid.UUID) -> tuple[list[Review], float, int]:
    rows = (
        db.query(Review)
        .filter(Review.target_id == target_id, Review.status == ReviewStatus.active)
        .order_by(Review.created_at.desc())
        .all()
    )
    total = len(rows)
    avg = round(sum(r.rating for r in rows) / total, 2) if total else 0.0
    return rows, avg, total


def _recompute_reputation(db: Session, user_id: uuid.UUID) -> None:
    """Set the target user's reputation to their average active rating (0-5)."""
    avg = db.scalar(
        select(func.avg(Review.rating)).where(
            Review.target_id == user_id, Review.status == ReviewStatus.active
        )
    )
    user = db.get(User, user_id)
    if user is not None and avg is not None:
        user.reputation_score = Decimal(str(round(float(avg), 2)))
