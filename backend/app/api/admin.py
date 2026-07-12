"""Admin back-office router: moderation queue, users, audit log.

Every mutating action is recorded in ``admin_actions`` for audit (SECURITY.md §7/§9).
No automated bans — admins act manually.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.errors import not_found
from app.db.session import get_db
from app.models.complaint import AdminAction, Complaint
from app.models.enums import (
    AdminActionType,
    AdminTargetType,
    ComplaintStatus,
)
from app.models.user import User
from app.schemas.admin import (
    AdminActionOut,
    AdminUserOut,
    ComplaintResolve,
    ReputationAdjust,
    SuspendRequest,
)
from app.schemas.interactions import ComplaintOut

router = APIRouter(prefix="/admin", tags=["admin"])


def _audit(
    db: Session,
    admin_id: uuid.UUID,
    action: AdminActionType,
    target_id: uuid.UUID,
    target_type: AdminTargetType,
    notes: str | None,
) -> None:
    db.add(
        AdminAction(
            admin_id=admin_id,
            action_type=action,
            target_id=target_id,
            target_type=target_type,
            notes=notes,
        )
    )


@router.get("/complaints", response_model=list[ComplaintOut])
def list_complaints(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    status_filter: ComplaintStatus | None = Query(default=None, alias="status"),
) -> list[ComplaintOut]:
    query = db.query(Complaint)
    if status_filter is not None:
        query = query.filter(Complaint.status == status_filter)
    rows = query.order_by(Complaint.created_at.desc()).limit(500).all()
    return [ComplaintOut.model_validate(c) for c in rows]


@router.put("/complaints/{complaint_id}/resolve", response_model=ComplaintOut)
def resolve_complaint(
    complaint_id: uuid.UUID,
    payload: ComplaintResolve,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> ComplaintOut:
    complaint = db.get(Complaint, complaint_id)
    if complaint is None:
        raise not_found("Complaint not found")
    complaint.status = payload.status
    complaint.admin_notes = payload.admin_notes
    complaint.reviewed_by = admin.id
    _audit(
        db,
        admin.id,
        AdminActionType.resolve_complaint,
        complaint.id,
        AdminTargetType.complaint,
        payload.admin_notes,
    )
    db.commit()
    db.refresh(complaint)
    return ComplaintOut.model_validate(complaint)


@router.get("/users", response_model=list[AdminUserOut])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    q: str | None = Query(default=None, max_length=100),
) -> list[AdminUserOut]:
    query = db.query(User)
    if q:
        like = f"%{q}%"
        query = query.filter((User.email.ilike(like)) | (User.phone.ilike(like)))
    rows = query.order_by(User.created_at.desc()).limit(500).all()
    return [AdminUserOut.model_validate(u) for u in rows]


@router.put("/users/{user_id}/suspend", response_model=AdminUserOut)
def suspend_user(
    user_id: uuid.UUID,
    payload: SuspendRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> AdminUserOut:
    user = db.get(User, user_id)
    if user is None:
        raise not_found("User not found")
    user.is_suspended = payload.suspended
    _audit(
        db,
        admin.id,
        AdminActionType.suspend,
        user.id,
        AdminTargetType.user,
        payload.notes,
    )
    db.commit()
    db.refresh(user)
    return AdminUserOut.model_validate(user)


@router.put("/users/{user_id}/reputation", response_model=AdminUserOut)
def adjust_reputation(
    user_id: uuid.UUID,
    payload: ReputationAdjust,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> AdminUserOut:
    user = db.get(User, user_id)
    if user is None:
        raise not_found("User not found")
    user.reputation_score = payload.reputation_score
    _audit(
        db,
        admin.id,
        AdminActionType.adjust_reputation,
        user.id,
        AdminTargetType.user,
        payload.notes,
    )
    db.commit()
    db.refresh(user)
    return AdminUserOut.model_validate(user)


@router.get("/actions", response_model=list[AdminActionOut])
def list_actions(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> list[AdminActionOut]:
    rows = db.query(AdminAction).order_by(AdminAction.created_at.desc()).limit(500).all()
    return [AdminActionOut.model_validate(a) for a in rows]
