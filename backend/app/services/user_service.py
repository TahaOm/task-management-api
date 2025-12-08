# app/services/user_service.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserFilter, UserLogin
from app.repositories.user import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from backend.app.core.config import settings


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(
        self, db: AsyncSession, user_data: UserCreate
    ) -> UserResponse:
        """Create a new user via service layer."""
        # Check if user already exists
        if await self.user_repository.email_exists(db, email=user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user via repository
        user = await self.user_repository.create_with_password(db, obj_in=user_data)
        return UserResponse.model_validate(user)

    async def get_user(self, db: AsyncSession, user_id: UUID) -> UserResponse:
        """Get user by ID via service layer."""
        user = await self.user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserResponse.model_validate(user)

    async def get_active_user(self, db: AsyncSession, user_id: UUID) -> UserResponse:
        """Get active user by ID via service layer."""
        user = await self.user_repository.get_active_user(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or inactive",
            )
        return UserResponse.model_validate(user)

    async def authenticate_user(
        self, db: AsyncSession, email: str, password: str
    ) -> UserResponse:
        """Authenticate user via service layer."""
        user = await self.user_repository.authenticate(
            db, email=email, password=password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return UserResponse.model_validate(user)

    async def login_user(self, db: AsyncSession, login_data: UserLogin) -> dict:
        """Login user and return tokens."""
        user = await self.authenticate_user(
            db, email=login_data.email, password=login_data.password
        )

        access_token = create_access_token(subject=str(user.id))

        return {"access_token": access_token, "token_type": "bearer", "user": user}

    async def update_user_profile(
        self, db: AsyncSession, user_id: UUID, profile_data: UserUpdate
    ) -> UserResponse:
        """Update user profile via service layer."""
        user = await self.user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        updated_user = await self.user_repository.update(
            db, db_obj=user, obj_in=profile_data
        )
        return UserResponse.model_validate(updated_user)

    async def update_password(
        self, db: AsyncSession, user_id: UUID, current_password: str, new_password: str
    ) -> bool:
        """Update user password with verification."""
        user = await self.user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # Update password
        return await self.user_repository.update_password(
            db, user_id=user_id, new_password=new_password
        )

    async def get_users_with_filter(
        self, db: AsyncSession, filter_data: UserFilter, skip: int = 0, limit: int = 100
    ) -> List[UserResponse]:
        """Get users with filtering via service layer."""
        filters = {}
        if filter_data.is_active is not None:
            filters["is_active"] = filter_data.is_active
        if filter_data.is_superuser is not None:
            filters["is_superuser"] = filter_data.is_superuser
        if filter_data.email:
            filters["email"] = filter_data.email

        users = await self.user_repository.get_multi(
            db, skip=skip, limit=limit, filters=filters, order_by="-created_at"
        )

        return [UserResponse.model_validate(user) for user in users]

    async def search_users(
        self, db: AsyncSession, query: str, skip: int = 0, limit: int = 50
    ) -> List[UserResponse]:
        """Search users via service layer."""
        users = await self.user_repository.search_users(
            db, query=query, skip=skip, limit=limit
        )
        return [UserResponse.model_validate(user) for user in users]

    async def activate_user(self, db: AsyncSession, user_id: UUID) -> UserResponse:
        """Activate user account via service layer."""
        success = await self.user_repository.activate_user(db, user_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user = await self.user_repository.get(db, id=user_id)
        return UserResponse.model_validate(user)

    async def deactivate_user(self, db: AsyncSession, user_id: UUID) -> UserResponse:
        """Deactivate user account via service layer."""
        success = await self.user_repository.deactivate_user(db, user_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user = await self.user_repository.get(db, id=user_id)
        return UserResponse.model_validate(user)
