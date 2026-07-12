"""Auth request/response schemas."""

from __future__ import annotations

import re
import uuid

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.models.enums import UserRole, VerificationMethod, VerificationStatus
from app.schemas.common import ORMModel

_PHONE_RE = re.compile(r"^\+?[0-9]{7,15}$")


class SignupRequest(BaseModel):
    email: EmailStr | None = None
    phone: str = Field(min_length=7, max_length=20)
    whatsapp: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.consumer
    verification_method: VerificationMethod = VerificationMethod.email

    @field_validator("phone", "whatsapp")
    @classmethod
    def _valid_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not _PHONE_RE.match(v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("role")
    @classmethod
    def _no_admin_signup(cls, v: UserRole) -> UserRole:
        if v == UserRole.admin:
            raise ValueError("Cannot self-register as admin")
        return v

    @model_validator(mode="after")
    def _method_requires_channel(self) -> SignupRequest:
        if self.verification_method == VerificationMethod.email and not self.email:
            raise ValueError("Email is required when verification_method is 'email'")
        if self.verification_method == VerificationMethod.whatsapp and not (
            self.whatsapp or self.phone
        ):
            raise ValueError("WhatsApp/phone required when verification_method is 'whatsapp'")
        return self


class SignupResponse(ORMModel):
    id: uuid.UUID
    email: str | None
    phone: str
    role: UserRole
    verification_status: VerificationStatus


class VerifyRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    code: str = Field(min_length=4, max_length=10)

    @model_validator(mode="after")
    def _need_identifier(self) -> VerifyRequest:
        if not self.email and not self.phone:
            raise ValueError("Provide email or phone")
        return self


class LoginRequest(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    password: str = Field(min_length=1, max_length=128)

    @model_validator(mode="after")
    def _need_identifier(self) -> LoginRequest:
        if not self.email and not self.phone:
            raise ValueError("Provide email or phone")
        return self


class UserPublic(ORMModel):
    id: uuid.UUID
    email: str | None
    phone: str
    role: UserRole
    verification_status: VerificationStatus


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
