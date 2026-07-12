"""Shared schema primitives."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ORMModel(BaseModel):
    """Base for response models read from ORM objects."""

    model_config = ConfigDict(from_attributes=True)


class GeoPoint(BaseModel):
    """GeoJSON Point: coordinates are [longitude, latitude]."""

    type: str = "Point"
    coordinates: list[float]


class LatLng(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class LocationInput(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    plus_code: str | None = Field(default=None, max_length=20)
    description: str | None = Field(default=None, max_length=2000)


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int
