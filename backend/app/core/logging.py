# app/core/logging.py
import logging
import sys
import logging.config
from app.core.config import settings


def setup_logging():
    """Setup application logging configuration."""

    # Determine log format based on environment
    log_format = (
        '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", '
        '"message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s"}'
        if settings.ENVIRONMENT == "production"
        else "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configure logging
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": log_format,
                    "datefmt": "%Y-%m-%d %H:%M:%S%z",
                },
                "json": {
                    "format": log_format,
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": (
                        "json" if settings.ENVIRONMENT == "production" else "default"
                    ),
                },
            },
            "root": {
                "level": settings.LOG_LEVEL.upper(),
                "handlers": ["console"],
            },
            "loggers": {
                "uvicorn": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": False,
                },
                "sqlalchemy.engine": {
                    "level": (
                        "WARNING" if settings.ENVIRONMENT == "production" else "INFO"
                    ),
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
    )
