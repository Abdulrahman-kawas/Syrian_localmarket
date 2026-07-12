"""Media upload router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.deps import get_verified_user
from app.core.config import settings
from app.core.errors import bad_request
from app.media.upload import process_upload
from app.models.user import User
from app.schemas.interactions import MediaUploadResponse

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/upload", response_model=MediaUploadResponse)
async def upload(
    file: UploadFile = File(...),
    _: User = Depends(get_verified_user),
) -> MediaUploadResponse:
    content_type = file.content_type or ""
    if content_type not in settings.allowed_image_types_set:
        raise bad_request("Unsupported image type")
    raw = await file.read()
    url, thumb_url = process_upload(raw, content_type)
    return MediaUploadResponse(url=url, thumbnail_url=thumb_url)
