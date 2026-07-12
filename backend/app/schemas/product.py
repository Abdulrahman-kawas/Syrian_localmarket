"""Product / listing schemas with pricing and food-safety validation."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from app.models.enums import ExpiryClass, ProductStatus, ProductType
from app.schemas.common import ORMModel
from app.schemas.seller import SellerSummary


class ProductCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    type: ProductType
    original_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    discounted_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    currency: str = Field(default="SYP", min_length=3, max_length=3)
    expiry_date: date | None = None
    expiry_class: ExpiryClass | None = None
    quantity: int = Field(ge=0)
    images: list[str] = Field(default_factory=list, max_length=10)

    @model_validator(mode="after")
    def _validate(self) -> ProductCreate:
        if self.discounted_price > self.original_price:
            raise ValueError("discounted_price cannot exceed original_price")
        # Food-safety: use_by items cannot be listed past their date.
        if (
            self.expiry_class == ExpiryClass.use_by
            and self.expiry_date is not None
            and self.expiry_date < date.today()
        ):
            raise ValueError("use_by items past their expiry date cannot be listed")
        return self


class ProductUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    type: ProductType | None = None
    original_price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    discounted_price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    expiry_date: date | None = None
    expiry_class: ExpiryClass | None = None
    quantity: int | None = Field(default=None, ge=0)
    images: list[str] | None = Field(default=None, max_length=10)
    status: ProductStatus | None = None


class QuantityUpdate(BaseModel):
    quantity: int = Field(ge=0)


class ProductOut(ORMModel):
    id: uuid.UUID
    seller_id: uuid.UUID
    type: ProductType
    title: str
    description: str | None
    images: list[str]
    original_price: Decimal
    discounted_price: Decimal
    currency: str
    expiry_date: date | None
    expiry_class: ExpiryClass | None
    quantity: int
    status: ProductStatus
    seller: SellerSummary | None = None
