"""Schemas for QR, reviews, complaints, chat, delivery, maps, media, notifications."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import (
    ComplaintTargetType,
    DeliveryStatus,
    DevicePlatform,
    ReviewTargetType,
)
from app.schemas.common import LatLng, LocationInput, ORMModel


# --- QR ----------------------------------------------------------------------
class QRCodeOut(BaseModel):
    code: str
    image_url: str | None = None


class QRScanRequest(BaseModel):
    code: str = Field(min_length=1, max_length=100)


class QRScanResponse(BaseModel):
    transaction_id: uuid.UUID
    status: str


class QRConfirmRequest(BaseModel):
    quantity: int = Field(gt=0)


class ProofRecord(BaseModel):
    buyer: uuid.UUID
    seller: uuid.UUID
    product: uuid.UUID
    quantity: int
    timestamp: datetime


class QRConfirmResponse(BaseModel):
    transaction_id: uuid.UUID
    status: str
    proof_record: ProofRecord


# --- Reviews -----------------------------------------------------------------
class ReviewCreate(BaseModel):
    target_id: uuid.UUID
    target_type: ReviewTargetType
    rating: int = Field(ge=1, le=5)
    text: str | None = Field(default=None, max_length=2000)


class ReviewOut(ORMModel):
    id: uuid.UUID
    author_id: uuid.UUID
    target_id: uuid.UUID
    target_type: ReviewTargetType
    rating: int
    text: str | None
    created_at: datetime


class ReviewList(BaseModel):
    items: list[ReviewOut]
    average_rating: float
    total_reviews: int


# --- Complaints --------------------------------------------------------------
class ComplaintCreate(BaseModel):
    target_id: uuid.UUID
    target_type: ComplaintTargetType
    listing_id: uuid.UUID | None = None
    reason: str = Field(min_length=3, max_length=2000)


class ComplaintOut(ORMModel):
    id: uuid.UUID
    reporter_id: uuid.UUID
    target_id: uuid.UUID
    target_type: ComplaintTargetType
    listing_id: uuid.UUID | None
    reason: str
    status: str
    created_at: datetime


# --- Chat --------------------------------------------------------------------
class ConversationCreate(BaseModel):
    participant_id: uuid.UUID


class ParticipantOut(BaseModel):
    id: uuid.UUID
    name: str


class ConversationOut(BaseModel):
    id: uuid.UUID
    participant: ParticipantOut


class ConversationSummary(BaseModel):
    """A conversation in the list view, with a preview of the latest message."""

    id: uuid.UUID
    participant: ParticipantOut
    last_message: str
    last_message_time: datetime


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class MessageOut(ORMModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    sender_id: uuid.UUID
    content: str
    created_at: datetime


class MessageList(BaseModel):
    items: list[MessageOut]


# --- Delivery ----------------------------------------------------------------
class DeliveryCreate(BaseModel):
    seller_id: uuid.UUID
    product_id: uuid.UUID | None = None
    location: LocationInput


class DeliveryOut(ORMModel):
    id: uuid.UUID
    consumer_id: uuid.UUID
    seller_id: uuid.UUID
    product_id: uuid.UUID | None
    location_description: str | None
    status: DeliveryStatus
    created_at: datetime


class DeliveryStatusUpdate(BaseModel):
    status: DeliveryStatus


# --- Maps --------------------------------------------------------------------
class DirectionsRequest(BaseModel):
    origin: LatLng
    destination: LatLng


class DirectionsResponse(BaseModel):
    distance: str
    duration: str
    directions_url: str


# --- Media -------------------------------------------------------------------
class MediaUploadResponse(BaseModel):
    url: str
    thumbnail_url: str


# --- Notifications -----------------------------------------------------------
class DeviceRegisterRequest(BaseModel):
    platform: DevicePlatform
    token: str = Field(min_length=1, max_length=500)


class OkResponse(BaseModel):
    ok: bool = True
