"""Image upload processing: validate, strip EXIF/GPS, resize, thumbnail, store."""

from __future__ import annotations

import io
import uuid

from PIL import Image, ImageOps, UnidentifiedImageError

from app.core.config import settings
from app.core.errors import bad_request
from app.media import storage

# Map Pillow formats to output content types.
_FORMAT_CONTENT_TYPE = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}
_MAX_DIM = 1600
_THUMB_DIM = 320


def _guess_format(declared_content_type: str) -> str:
    if declared_content_type == "image/png":
        return "PNG"
    if declared_content_type == "image/webp":
        return "WEBP"
    return "JPEG"


def process_upload(raw: bytes, declared_content_type: str) -> tuple[str, str]:
    """Validate and normalise an uploaded image; return (url, thumbnail_url).

    Security controls (SECURITY.md §3):
      * size limit enforced,
      * real image validated via Pillow (magic bytes, not just declared type),
      * EXIF/GPS metadata stripped by re-encoding from pixel data only,
      * output re-encoded to a known-safe format.
    """
    if len(raw) == 0:
        raise bad_request("Empty file")
    if len(raw) > settings.max_upload_size_bytes:
        raise bad_request(
            f"File exceeds {settings.max_upload_size_mb}MB limit",
            {"max_mb": settings.max_upload_size_mb},
        )
    if declared_content_type not in settings.allowed_image_types_set:
        raise bad_request("Unsupported image type")

    try:
        img = Image.open(io.BytesIO(raw))
        img.verify()  # verify magic bytes / integrity
        img = Image.open(io.BytesIO(raw))  # reopen: verify() leaves it unusable
    except (UnidentifiedImageError, OSError) as exc:
        raise bad_request("File is not a valid image") from exc

    # Honour EXIF orientation, then drop ALL metadata by copying pixel data.
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))

    out_format = _guess_format(declared_content_type)
    content_type = _FORMAT_CONTENT_TYPE[out_format]
    ext = content_type.split("/")[1]
    key = uuid.uuid4().hex

    main_bytes = _encode(clean, out_format, _MAX_DIM)
    thumb_bytes = _encode(clean, out_format, _THUMB_DIM)

    url = storage.save_bytes(main_bytes, f"{key}.{ext}", content_type)
    thumb_url = storage.save_bytes(thumb_bytes, f"{key}_thumb.{ext}", content_type)
    return url, thumb_url


def _encode(img: Image.Image, out_format: str, max_dim: int) -> bytes:
    work = img.copy()
    work.thumbnail((max_dim, max_dim), Image.LANCZOS)
    if out_format == "JPEG" and work.mode == "RGBA":
        work = work.convert("RGB")
    buf = io.BytesIO()
    save_kwargs = {"format": out_format}
    if out_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = 85
    work.save(buf, **save_kwargs)  # no exif passed => metadata stripped
    return buf.getvalue()
