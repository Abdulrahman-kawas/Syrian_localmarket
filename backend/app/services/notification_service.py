"""Push notification registration and delivery via Azure Notification Hubs.

Local/dev behaviour: registrations persist in Postgres and pushes are logged.
Production: set AZURE_NOTIFICATION_HUBS_CONNECTION_STRING to enable real sends.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.device import DeviceRegistration
from app.models.enums import DevicePlatform
from app.services import notification_hub

logger = get_logger("app.notifications")


def register_device(
    db: Session, user_id: uuid.UUID, platform: DevicePlatform, token: str
) -> DeviceRegistration:
    """Idempotently store a push token for a user/device."""
    existing = db.query(DeviceRegistration).filter(DeviceRegistration.token == token).one_or_none()
    if existing is not None:
        existing.user_id = user_id
        existing.platform = platform
        db.commit()
        db.refresh(existing)
        return existing

    reg = DeviceRegistration(user_id=user_id, platform=platform, token=token)
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg


def tokens_for_user(db: Session, user_id: uuid.UUID) -> list[str]:
    rows = db.query(DeviceRegistration).filter(DeviceRegistration.user_id == user_id).all()
    return [r.token for r in rows]


def send_to_user(
    db: Session, user_id: uuid.UUID, title: str, body: str, data: dict[str, Any] | None = None
) -> int:
    """Send a push to all of a user's devices (platform-aware). Returns count."""
    rows = db.query(DeviceRegistration).filter(DeviceRegistration.user_id == user_id).all()
    payload = data or {}
    for reg in rows:
        _send_one(reg.token, reg.platform.value, title, body, payload)
    return len(rows)


def _send_one(token: str, platform: str, title: str, body: str, data: dict[str, Any]) -> None:
    """Deliver one push, or log a no-op when Notification Hubs isn't configured."""
    if not notification_hub.is_configured():
        logger.info("push_noop", extra={"extra_fields": {"platform": platform, "title": title}})
        return
    notification_hub.send_direct(token, platform, title, body, data)


def _dispatch(tokens: list[str], title: str, body: str, data: dict[str, Any]) -> None:
    """Broadcast helper (platform unknown → default fcm). Used by timer jobs."""
    if not notification_hub.is_configured():
        logger.info("push_noop", extra={"extra_fields": {"tokens": len(tokens), "title": title}})
        return
    for token in tokens:
        notification_hub.send_direct(token, "fcm", title, body, data)
