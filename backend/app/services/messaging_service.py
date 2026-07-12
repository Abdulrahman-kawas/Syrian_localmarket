"""Outbound messaging: verification codes via email (ACS) or WhatsApp (ACS).

Real providers are used when configured; otherwise delivery falls back to a
server-side log (dev), so the stack runs end-to-end on a laptop with no secrets.
The verification code itself is never logged in production.
"""

from __future__ import annotations

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.messaging")


def send_email(to: str, subject: str, body: str) -> bool:
    """Send a plain-text email. Returns True if actually dispatched."""
    if not settings.acs_connection_string:
        logger.info("email_noop", extra={"extra_fields": {"to_domain": _domain(to)}})
        return False
    try:
        from azure.communication.email import EmailClient

        client = EmailClient.from_connection_string(settings.acs_connection_string)
        message = {
            "senderAddress": settings.acs_sender_email,
            "recipients": {"to": [{"address": to}]},
            "content": {"subject": subject, "plainText": body},
        }
        poller = client.begin_send(message)
        poller.result()
        logger.info("email_sent", extra={"extra_fields": {"to_domain": _domain(to)}})
        return True
    except Exception as exc:  # noqa: BLE001 - never let delivery break signup
        logger.error("email_send_failed", exc_info=exc)
        return False


def send_whatsapp(to: str, body: str) -> bool:
    """Send a WhatsApp text via ACS Advanced Messaging. True if dispatched."""
    if not (settings.acs_connection_string and settings.acs_whatsapp_channel_id):
        logger.info("whatsapp_noop", extra={"extra_fields": {"to_suffix": to[-4:]}})
        return False
    try:
        from azure.communication.messages import NotificationMessagesClient
        from azure.communication.messages.models import TextNotificationContent

        client = NotificationMessagesClient.from_connection_string(
            settings.acs_connection_string
        )
        client.send(
            TextNotificationContent(
                channel_registration_id=settings.acs_whatsapp_channel_id,
                to=[to],
                content=body,
            )
        )
        logger.info("whatsapp_sent", extra={"extra_fields": {"to_suffix": to[-4:]}})
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("whatsapp_send_failed", exc_info=exc)
        return False


def send_verification_code(
    *, method: str, email: str | None, phone: str | None, code: str
) -> None:
    """Deliver a verification code via the user's chosen channel."""
    subject = "Your LocalMarket verification code"
    body = f"Your LocalMarket verification code is: {code}"
    if method == "whatsapp" and (phone or email):
        send_whatsapp(phone or "", body)
    elif email:
        send_email(email, subject, body)
    else:
        logger.info("verification_delivery_skipped_no_channel")


def _domain(email: str) -> str:
    return email.split("@")[-1] if "@" in email else "?"
