"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/srotgraph"
    database_url_sync: str = "postgresql://postgres:postgres@localhost:5432/srotgraph"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI Providers
    speech_recognition_provider: str = "mock"
    claim_extraction_provider: str = "mock"
    retrieval_provider: str = "mock"

    # Provider API Keys (optional, only needed for non-mock providers)
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    deepgram_api_key: str | None = None
    assemblyai_api_key: str | None = None

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app_env == "development"


settings = Settings()
