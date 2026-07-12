"""Admin back-office schemas."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import ComplaintStatus, UserRole, VerificationStatus
from app.schemas.common import ORMModel


class AdminUserOut(ORMModel):
    id: uuid.UUID
    email: str | None
    phone: str
    role: UserRole
    verification_status: VerificationStatus
    reputation_score: Decimal
    is_suspended: bool
    created_at: datetime


class ComplaintResolve(BaseModel):
    status: ComplaintStatus
    admin_notes: str | None = Field(default=None, max_length=2000)


class ReputationAdjust(BaseModel):
    reputation_score: Decimal = Field(ge=0, le=5, max_digits=3, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class SuspendRequest(BaseModel):
    suspended: bool
    notes: str | None = Field(default=None, max_length=2000)


class AdminActionOut(ORMModel):
    id: uuid.UUID
    admin_id: uuid.UUID
    action_type: str
    target_id: uuid.UUID
    target_type: str
    notes: str | None
    created_at: datetime
