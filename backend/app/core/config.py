from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import secrets
import logging

# Configure logger
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,  # Changed to True for consistency
        extra="ignore",
        env_prefix="",
        validate_assignment=True,  # Validate when attributes are set
    )

    # Application
    PROJECT_NAME: str = Field(
        default="Task Management API", description="Name of the application"
    )
    VERSION: str = Field(default="1.0.0", description="Application version")
    API_V1_STR: str = Field(default="/api/v1", description="API version prefix")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(
        default="development",
        description="Runtime environment",
        pattern="^(development|staging|production|testing)$",
    )

    # Database
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="PostgreSQL database URL",
        examples=["postgresql+asyncpg://user:pass@localhost:5432/dbname"],
    )

    # Redis
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection URL",
        examples=["redis://localhost:6379/0"],
    )

    # Security
    SECRET_KEY: Optional[str] = Field(
        default=None, description="JWT secret key for token signing", min_length=32
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, ge=1, description="Access token expiration in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7, ge=1, description="Refresh token expiration in days"
    )

    # Celery
    CELERY_BROKER_URL: Optional[str] = Field(
        default=None, description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: Optional[str] = Field(
        default=None, description="Celery result backend URL"
    )

    # Email
    SENDGRID_API_KEY: Optional[str] = Field(
        default=None, description="SendGrid API key for email service"
    )
    FROM_EMAIL: str = Field(
        default="noreply@example.com", description="Default sender email address"
    )

    # CORS
    FRONTEND_URL: str = Field(
        default="http://localhost:3000", description="Frontend application URL"
    )
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins",
    )

    # Pagination
    DEFAULT_PAGE_SIZE: int = Field(
        default=20, ge=1, le=1000, description="Default number of items per page"
    )
    MAX_PAGE_SIZE: int = Field(
        default=100, ge=1, le=1000, description="Maximum number of items per page"
    )

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60, ge=1, description="Maximum requests per minute"
    )

    # Logging
    LOG_LEVEL: str = Field(
        default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )

    # Security
    ALLOWED_HOSTS: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "0.0.0.0"],
        description="Allowed hostnames",
    )
    TRUSTED_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Trusted origins for security",
    )

    @model_validator(mode="after")
    def set_defaults_and_validate(self) -> "Settings":
        """Set default values and validate configuration."""

        # Log environment initialization
        logger.info(f"Initializing settings for {self.ENVIRONMENT} environment")

        # Set default DATABASE_URL
        if not self.DATABASE_URL:
            if self.is_development:
                self.DATABASE_URL = (
                    "postgresql+asyncpg://taskuser:taskpass@localhost:5432/taskdb"
                )
                logger.warning("Using default development database URL")
            else:
                raise ValueError("DATABASE_URL is required in production")

        # Set default SECRET_KEY
        if not self.SECRET_KEY:
            if self.is_development:
                self.SECRET_KEY = f"dev-key-{secrets.token_urlsafe(32)}"
                logger.warning("Using auto-generated development SECRET_KEY")
            else:
                raise ValueError("SECRET_KEY is required in production")

        # Validate SECRET_KEY in production
        if self.is_production:
            if len(self.SECRET_KEY) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters in production"
                )
            if "dev-key" in self.SECRET_KEY:
                raise ValueError("Cannot use development SECRET_KEY in production")

        # Set Redis and Celery defaults
        self._set_redis_defaults()
        self._set_celery_defaults()

        # Validate CORS origins in production
        if self.is_production:
            self._validate_production_settings()

        logger.info("Settings initialization completed successfully")
        return self

    def _set_redis_defaults(self) -> None:
        """Set Redis-related defaults."""
        if not self.REDIS_URL:
            self.REDIS_URL = "redis://localhost:6379/0"
            if self.is_development:
                logger.warning("Using default Redis URL for development")

    def _set_celery_defaults(self) -> None:
        """Set Celery-related defaults."""
        if not self.CELERY_BROKER_URL and self.REDIS_URL:
            self.CELERY_BROKER_URL = self.REDIS_URL.replace("/0", "/1")

        if not self.CELERY_RESULT_BACKEND and self.REDIS_URL:
            self.CELERY_RESULT_BACKEND = self.REDIS_URL.replace("/0", "/2")

    def _validate_production_settings(self) -> None:
        """Validate production-specific settings."""
        if not self.SENDGRID_API_KEY:
            logger.warning(
                "SENDGRID_API_KEY not set - email functionality will be disabled"
            )

        if "localhost" in self.FRONTEND_URL:
            logger.warning("Using localhost in FRONTEND_URL in production")

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    @property
    def is_staging(self) -> bool:
        return self.ENVIRONMENT == "staging"

    def get_database_url_async(self) -> str:
        """Get async database URL."""
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgresql://"):
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return self.DATABASE_URL or ""

    def get_cors_origins(self) -> list[str]:
        """Get CORS origins including frontend URL."""
        origins = set(self.BACKEND_CORS_ORIGINS)
        origins.add(self.FRONTEND_URL)
        return list(origins)

    def __str__(self) -> str:
        """Safe string representation excluding sensitive data."""
        return f"Settings(environment={self.ENVIRONMENT}, debug={self.DEBUG})"


# Global settings instance - THIS IS THE LATEST BEST PRACTICE
settings = Settings()


# Optional: Function to get settings (useful for testing)
def get_settings() -> Settings:
    """Get settings instance (useful for dependency injection)."""
    return settings
