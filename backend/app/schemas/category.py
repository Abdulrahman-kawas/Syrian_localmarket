"""Category schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class CategoryOut(ORMModel):
    id: uuid.UUID
    name_ar: str
    name_en: str
    slug: str
    active: bool


class CategoryCreate(BaseModel):
    name_ar: str = Field(min_length=1, max_length=100)
    name_en: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100, pattern=r"^[a-z0-9\-]+$")
