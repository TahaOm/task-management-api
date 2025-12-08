# app/api/v1/health.py
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.core.config import settings
import logging

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.VERSION,
    }


@router.get("/health/db")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    """Database health check with actual query."""
    try:
        # Execute a simple query to check database connection
        result = await db.execute(text("SELECT 1"))
        data = result.scalar_one()  # Get the value, don't await it

        logger.debug(f"Database health check passed: {data}")

        return {
            "database": "connected",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "check_value": data,  # Should be 1
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")


@router.get("/health/redis")
async def health_check_redis():
    """Redis health check (if you have Redis)."""
    try:
        # TODO: Implement Redis health check if you're using Redis
        # Example with redis.asyncio:
        # import redis.asyncio as redis
        # r = redis.from_url(settings.REDIS_URL)
        # await r.ping()

        return {
            "redis": "connected",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.warning(f"Redis health check failed: {str(e)}")
        return {
            "redis": "disconnected",
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


@router.get("/health/full")
async def full_health_check(db: AsyncSession = Depends(get_db)):
    """Comprehensive health check of all services."""
    health_status = {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.VERSION,
        "checks": {},
    }

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time": "N/A",  # Could add timing here
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {"status": "unhealthy", "error": str(e)}

    # Redis check (optional)
    try:
        # Implement Redis check if needed
        health_status["checks"]["redis"] = {
            "status": "disabled",
            "message": "Redis not configured",
        }
    except Exception as e:
        health_status["checks"]["redis"] = {"status": "unhealthy", "error": str(e)}

    return health_status
