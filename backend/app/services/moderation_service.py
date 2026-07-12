"""Text sanitisation and lightweight content moderation."""

from __future__ import annotations

import bleach

# Free text is plain text in this app: strip *all* HTML tags and attributes.
_ALLOWED_TAGS: list[str] = []
_ALLOWED_ATTRS: dict[str, list[str]] = {}


def sanitize_text(value: str | None) -> str | None:
    """Remove any HTML/script content from user-supplied free text (XSS defence)."""
    if value is None:
        return None
    cleaned = bleach.clean(
        value,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRS,
        strip=True,
    )
    return cleaned.strip()
