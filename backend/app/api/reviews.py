"""Reviews router."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_verified_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.interactions import ReviewCreate, ReviewList, ReviewOut
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    payload: ReviewCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> ReviewOut:
    review = review_service.create(db, user, payload)
    return ReviewOut.model_validate(review)


@router.get("/{target_id}", response_model=ReviewList)
def list_reviews(target_id: uuid.UUID, db: Session = Depends(get_db)) -> ReviewList:
    rows, avg, total = review_service.list_for_target(db, target_id)
    return ReviewList(
        items=[ReviewOut.model_validate(r) for r in rows],
        average_rating=avg,
        total_reviews=total,
    )
