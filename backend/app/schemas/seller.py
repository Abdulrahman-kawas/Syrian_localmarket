"""Seller profile schemas."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from app.models.enums import SellerType
from app.schemas.common import GeoPoint, LocationInput, ORMModel


class SellerOnboardRequest(BaseModel):
    type: SellerType
    shop_name: str = Field(min_length=1, max_length=100)
    category_id: uuid.UUID | None = None
    location: LocationInput
    shop_photo_url: str | None = Field(default=None, max_length=500)
    personal_photo_url: str | None = Field(default=None, max_length=500)
    exterior_photos: list[str] = Field(default_factory=list, max_length=10)


class SellerUpdateRequest(BaseModel):
    shop_name: str | None = Field(default=None, min_length=1, max_length=100)
    category_id: uuid.UUID | None = None
    location: LocationInput | None = None
    shop_photo_url: str | None = Field(default=None, max_length=500)
    personal_photo_url: str | None = Field(default=None, max_length=500)
    exterior_photos: list[str] | None = Field(default=None, max_length=10)


class SellerOut(ORMModel):
    id: uuid.UUID
    type: SellerType
    shop_name: str
    category_id: uuid.UUID | None
    geo_point: GeoPoint | None
    plus_code: str | None
    location_description: str | None
    shop_photo_url: str | None
    personal_photo_url: str | None
    exterior_photos: list[str]


class SellerSummary(ORMModel):
    """Compact seller info embedded in product/search responses."""

    id: uuid.UUID
    user_id: uuid.UUID
    shop_name: str
    type: SellerType
    phone: str | None = None
