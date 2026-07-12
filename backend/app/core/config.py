"""Application configuration loaded from environment / Key Vault."""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object. Secrets come from env or Azure Key Vault."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me-in-production"
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+psycopg2://localmarket:localmarket@localhost:5432/localmarket"

    # Auth / JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60
    auth_rate_limit_requests: int = 10
    auth_rate_limit_window_seconds: int = 60

    # File uploads
    max_upload_size_mb: int = 10
    allowed_image_types: str = "image/jpeg,image/png,image/webp"
    # Local media dir used when Azure Blob is not configured (relative to CWD).
    local_media_root: str = "media_store"

    # Azure Storage / CDN
    azure_storage_connection_string: str = ""
    azure_storage_account_name: str = ""
    azure_storage_container: str = "media"
    azure_cdn_endpoint: str = ""

    # Azure Communication Services (email + WhatsApp advanced messaging)
    acs_connection_string: str = ""
    acs_sender_email: str = "noreply@localmarket.app"
    acs_whatsapp_channel_id: str = ""

    # Azure Notification Hubs
    azure_notification_hubs_connection_string: str = ""
    azure_notification_hubs_hub_name: str = ""

    # Azure SignalR
    azure_signalr_connection_string: str = ""
    azure_signalr_hub_name: str = "chat"

    # Google Maps (server-side only)
    google_maps_api_key: str = ""

    # Monitoring
    applicationinsights_connection_string: str = ""

    # CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:19006",
            "http://localhost:5173",
        ]
    )

    # Proximity notifications
    proximity_radius_km: float = 5.0

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, value: object) -> object:
        """Accept a comma-separated string as well as a JSON list from env."""
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.startswith("["):
                return value  # let pydantic parse JSON
            return [o.strip() for o in stripped.split(",") if o.strip()]
        return value

    @property
    def allowed_image_types_set(self) -> set[str]:
        return {t.strip() for t in self.allowed_image_types.split(",") if t.strip()}

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()


settings = get_settings()
