# app/api/v1/__init__.py
from fastapi import APIRouter
from app.core.config import settings

# Import all your routers
from .health import router as health_router

# Import other routers as you implement them
# from .auth import router as auth_router
# from .users import router as users_router
# from .projects import router as projects_router
# from .tasks import router as tasks_router
# from .comments import router as comments_router
# from .notifications import router as notifications_router
# from .websocket import router as websocket_router

# Create version 1 router
v1_router = APIRouter(prefix=settings.API_V1_STR)

# Include all routers under v1 prefix
v1_router.include_router(health_router, tags=["health"])
# v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
# v1_router.include_router(users_router, prefix="/users", tags=["users"])
# v1_router.include_router(projects_router, prefix="/projects", tags=["projects"])
# v1_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
# v1_router.include_router(comments_router, prefix="/comments", tags=["comments"])
# v1_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
# v1_router.include_router(websocket_router, prefix="/ws", tags=["websocket"])

__all__ = ["v1_router"]
