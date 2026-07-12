"""Storage backends for processed media.

Azure Blob Storage when configured (production); local filesystem otherwise so the
stack runs end-to-end on a laptop via Docker. Local files are served at ``/media``.
"""

from __future__ import annotations

import contextlib
from pathlib import Path

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.media.storage")

# Local fallback directory (mounted as a Docker volume in compose).
LOCAL_MEDIA_ROOT = Path(settings.local_media_root)
LOCAL_MEDIA_URL_PREFIX = "/media"


def _use_azure() -> bool:
    return bool(settings.azure_storage_connection_string)


def save_bytes(data: bytes, blob_name: str, content_type: str) -> str:
    """Persist bytes and return a publicly-reachable URL."""
    if _use_azure():
        return _save_azure(data, blob_name, content_type)
    return _save_local(data, blob_name)


def _save_local(data: bytes, blob_name: str) -> str:
    dest = LOCAL_MEDIA_ROOT / blob_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return f"{LOCAL_MEDIA_URL_PREFIX}/{blob_name}"


def _save_azure(data: bytes, blob_name: str, content_type: str) -> str:
    from azure.storage.blob import BlobServiceClient, ContentSettings

    client = BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)
    container = client.get_container_client(settings.azure_storage_container)
    with contextlib.suppress(Exception):  # container already exists is fine
        container.create_container()
    blob = container.get_blob_client(blob_name)
    blob.upload_blob(
        data,
        overwrite=True,
        content_settings=ContentSettings(content_type=content_type),
    )
    if settings.azure_cdn_endpoint:
        base = settings.azure_cdn_endpoint.rstrip("/")
        return f"{base}/{settings.azure_storage_container}/{blob_name}"
    return blob.url
