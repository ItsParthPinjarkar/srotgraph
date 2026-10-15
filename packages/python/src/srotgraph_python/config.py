"""Shared configuration utilities for SrotGraph."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettings(BaseSettings):
    """Base settings class with common configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


class AppSettings(BaseSettings):
    """Application-level settings."""

    app_name: str = "SrotGraph"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"
