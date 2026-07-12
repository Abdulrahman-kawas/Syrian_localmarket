"""Azure Notification Hubs data-plane client (SAS auth + REST direct send).

No official Python data-plane SDK exists, so this signs requests with a SAS
token and POSTs directly to the hub. Used only when a connection string is
configured; callers fall back to a no-op/log otherwise.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.notification_hub")

_API_VERSION = "2015-01"


def is_configured() -> bool:
    return bool(
        settings.azure_notification_hubs_connection_string
        and settings.azure_notification_hubs_hub_name
    )


def _parse_connection_string(conn: str) -> tuple[str, str, str]:
    parts = dict(p.split("=", 1) for p in conn.split(";") if "=" in p)
    endpoint = parts["Endpoint"].replace("sb://", "https://").rstrip("/")
    return endpoint, parts["SharedAccessKeyName"], parts["SharedAccessKey"]


def _sas_token(uri: str, key_name: str, key: str, ttl_seconds: int = 3600) -> str:
    encoded_uri = urllib.parse.quote_plus(uri.lower())
    expiry = int(time.time()) + ttl_seconds
    to_sign = f"{encoded_uri}\n{expiry}".encode()
    signature = base64.b64encode(hmac.new(key.encode("utf-8"), to_sign, hashlib.sha256).digest())
    sig = urllib.parse.quote_plus(signature)
    return f"SharedAccessSignature sr={encoded_uri}&sig={sig}&se={expiry}&skn={key_name}"


def send_direct(token: str, platform: str, title: str, body: str, data: dict[str, Any]) -> bool:
    """Send a notification straight to one device handle. True if accepted."""
    endpoint, key_name, key = _parse_connection_string(
        settings.azure_notification_hubs_connection_string
    )
    hub = settings.azure_notification_hubs_hub_name
    uri = f"{endpoint}/{hub}"
    url = f"{uri}/messages/?direct&api-version={_API_VERSION}"

    if platform == "apns":
        fmt = "apple"
        payload: dict[str, Any] = {
            "aps": {"alert": {"title": title, "body": body}},
            "data": data,
        }
    else:  # fcm / gcm
        fmt = "gcm"
        payload = {"notification": {"title": title, "body": body}, "data": data}

    headers = {
        "Authorization": _sas_token(uri, key_name, key),
        "Content-Type": "application/json;charset=utf-8",
        "ServiceBusNotification-Format": fmt,
        "ServiceBusNotification-DeviceHandle": token,
    }
    try:
        resp = httpx.post(url, headers=headers, json=payload, timeout=8.0)
        resp.raise_for_status()
        return True
    except httpx.HTTPError as exc:
        logger.error("nh_send_failed", exc_info=exc)
        return False
