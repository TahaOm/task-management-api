from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Application
    PROJECT_NAME: str = "Task Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str | None = None
    
    # Redis
    REDIS_URL: str | None = None
    
    # Security
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Celery
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None
    
    # Email
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@example.com"
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    @model_validator(mode="after")
    def validate_required(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is required")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is required")
        return self

# Create global settings instance
settings = Settings()