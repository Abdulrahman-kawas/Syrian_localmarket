"""Structured error envelope and exception handlers (matches docs/API.md)."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger("app.errors")


class AppError(Exception):
    """Domain error carrying an HTTP status, machine code and safe message."""

    def __init__(
        self,
        message: str,
        code: str = "ERROR",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


# Convenience factories for common cases -------------------------------------
def not_found(message: str = "Resource not found") -> AppError:
    return AppError(message, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


def forbidden(message: str = "Not authorized") -> AppError:
    return AppError(message, code="FORBIDDEN", status_code=status.HTTP_403_FORBIDDEN)


def unauthorized(message: str = "Authentication required") -> AppError:
    return AppError(message, code="UNAUTHORIZED", status_code=status.HTTP_401_UNAUTHORIZED)


def conflict(message: str = "Conflict") -> AppError:
    return AppError(message, code="CONFLICT", status_code=status.HTTP_409_CONFLICT)


def bad_request(message: str, details: dict[str, Any] | None = None) -> AppError:
    return AppError(
        message, code="VALIDATION_ERROR", status_code=status.HTTP_400_BAD_REQUEST, details=details
    )


def _envelope(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return body


def register_error_handlers(app: FastAPI) -> None:
    """Attach handlers that return the standard error envelope for all failures."""

    @app.exception_handler(AppError)
    async def _handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = {
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            409: "CONFLICT",
            429: "RATE_LIMITED",
        }.get(exc.status_code, "ERROR")
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return JSONResponse(status_code=exc.status_code, content=_envelope(code, message))

    @app.exception_handler(RequestValidationError)
    async def _handle_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0] if exc.errors() else {}
        field = ".".join(str(p) for p in first.get("loc", []) if p != "body")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope(
                "VALIDATION_ERROR",
                "Invalid input",
                {"field": field, "issue": first.get("msg", "invalid")},
            ),
        )

    @app.exception_handler(Exception)
    async def _handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        # Never leak stack traces to clients; log server-side only.
        logger.error("unhandled_exception", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope("INTERNAL_ERROR", "An unexpected error occurred"),
        )
