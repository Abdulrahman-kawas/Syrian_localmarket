"""Complaints router (report queue; no auto-ban)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_verified_user
from app.db.session import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.schemas.interactions import ComplaintCreate, ComplaintOut
from app.services.moderation_service import sanitize_text

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post("", response_model=ComplaintOut, status_code=status.HTTP_201_CREATED)
def file_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_verified_user),
) -> ComplaintOut:
    complaint = Complaint(
        reporter_id=user.id,
        target_id=payload.target_id,
        target_type=payload.target_type,
        listing_id=payload.listing_id,
        reason=sanitize_text(payload.reason) or payload.reason,
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return ComplaintOut.model_validate(complaint)
