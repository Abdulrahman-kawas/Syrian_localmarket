"""Lightweight in-memory sliding-window rate limiter.

Single-instance friendly (local Docker, one container). For multi-instance Azure
deployments back this with Redis by swapping `_Bucket` for a shared store.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque

from fastapi import Request

from app.core.config import settings
from app.core.errors import AppError


class _SlidingWindow:
    """Thread-safe per-key sliding window counter."""

    def __init__(self) -> None:
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def hit(self, key: str, limit: int, window_seconds: int) -> bool:
        """Record a hit. Return True if allowed, False if the limit is exceeded."""
        now = time.monotonic()
        cutoff = now - window_seconds
        with self._lock:
            q = self._events[key]
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= limit:
                return False
            q.append(now)
            return True


_store = _SlidingWindow()


def _client_key(request: Request, scope: str) -> str:
    client = request.client.host if request.client else "unknown"
    # If behind Azure Front Door / a proxy, honour the forwarded client IP.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        client = forwarded.split(",")[0].strip()
    return f"{scope}:{client}"


class RateLimiter:
    """FastAPI dependency enforcing a request budget per client IP."""

    def __init__(self, times: int, seconds: int, scope: str = "default") -> None:
        self.times = times
        self.seconds = seconds
        self.scope = scope

    async def __call__(self, request: Request) -> None:
        if not settings.rate_limit_enabled:
            return
        key = _client_key(request, self.scope)
        if not _store.hit(key, self.times, self.seconds):
            raise AppError(
                "Too many requests, please slow down",
                code="RATE_LIMITED",
                status_code=429,
                details={"retry_after_seconds": self.seconds},
            )


# Shared limiter instances -----------------------------------------------------
default_rate_limit = RateLimiter(
    settings.rate_limit_requests, settings.rate_limit_window_seconds, scope="default"
)
# Stricter budget for auth endpoints — brute-force protection.
auth_rate_limit = RateLimiter(
    settings.auth_rate_limit_requests, settings.auth_rate_limit_window_seconds, scope="auth"
)
