"""FastAPI application entry point and factory."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app import __version__
from app.api import api_router
from app.core.config import settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.media.storage import LOCAL_MEDIA_ROOT, LOCAL_MEDIA_URL_PREFIX


def create_app() -> FastAPI:
    configure_logging("DEBUG" if settings.app_debug else "INFO")

    app = FastAPI(
        title="LocalMarket API",
        version=__version__,
        description="Syrian marketplace backend — discovery & connection, no in-app payments.",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url=None,
    )

    # Security headers / host allow-list (relaxed in dev).
    if settings.is_production:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_error_handlers(app)
    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    _mount_local_media(app)
    return app


def _mount_local_media(app: FastAPI) -> None:
    """Serve locally-stored media when Azure Blob is not configured."""
    if settings.azure_storage_connection_string:
        return
    from fastapi.staticfiles import StaticFiles

    Path(LOCAL_MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
    app.mount(
        LOCAL_MEDIA_URL_PREFIX,
        StaticFiles(directory=str(LOCAL_MEDIA_ROOT)),
        name="media",
    )


app = create_app()
