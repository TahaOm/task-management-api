# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.services.user_service import UserService
from app.core.security import get_user_id_from_token
import uuid

from backend.app.db.session import get_db
from backend.app.schemas.user import UserResponse

# Security scheme for Bearer tokens
security = HTTPBearer(auto_error=False)


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository()


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Get current authenticated user from JWT token.

    This dependency:
    1. Extracts token from Authorization header
    2. Validates the token
    3. Gets user from database
    4. Returns UserResponse or raises 401
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate token and extract user ID
    user_id_str = get_user_id_from_token(credentials.credentials)
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier in token",
        )

    # Get user from database using service layer
    try:
        user = await user_service.get_active_user(db, user_id)
        return user
    except HTTPException as e:
        # Re-raise if it's a 404 (user not found)
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise


async def get_current_active_superuser(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """
    Get current superuser. Raises 403 if user is not superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBORBIDDEN,
            detail="Superuser privileges required",
        )
    return current_user


async def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    user_service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db),
) -> UserResponse | None:
    """
    Get current user if authenticated, otherwise return None.
    Useful for endpoints that work for both authenticated and unauthenticated users.
    """
    if not credentials:
        return None

    user_id_str = get_user_id_from_token(credentials.credentials)
    if not user_id_str:
        return None

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        return None

    try:
        user = await user_service.get_active_user(db, user_id)
        return user
    except HTTPException:
        return None
