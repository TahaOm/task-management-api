from typing import List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.repositories import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User-specific repository with custom user operations"""

    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email address"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_active_user(
        self, db: AsyncSession, user_id: uuid.UUID
    ) -> Optional[User]:
        """Get active user by ID"""
        result = await db.execute(
            select(User).where(and_(User.id == user_id, User.is_active == True))
        )
        return result.scalar_one_or_none()

    async def create_with_password(
        self, db: AsyncSession, *, obj_in: UserCreate
    ) -> User:
        """Create user with hashed password"""
        # Hash password before saving
        create_data = obj_in.model_dump(exclude={"password"})
        create_data["hashed_password"] = get_password_hash(obj_in.password)

        db_obj = User(**create_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_password(
        self, db: AsyncSession, user_id: uuid.UUID, new_password: str
    ) -> bool:
        """Update user password"""
        user = await self.get(db, user_id)
        if not user:
            return False

        user.hashed_password = get_password_hash(new_password)
        await db.commit()
        await db.refresh(user)
        return True

    async def deactivate_user(self, db: AsyncSession, user_id: uuid.UUID) -> bool:
        """Deactivate user account"""
        user = await self.get(db, user_id)
        if not user:
            return False

        user.is_active = False
        await db.commit()
        await db.refresh(user)
        return True

    async def activate_user(self, db: AsyncSession, user_id: uuid.UUID) -> bool:
        """Activate user account"""
        user = await self.get(db, user_id)
        if not user:
            return False

        user.is_active = True
        await db.commit()
        await db.refresh(user)
        return True

    async def search_users(
        self, db: AsyncSession, query: str, skip: int = 0, limit: int = 50
    ) -> List[User]:
        """Search users by email or name"""
        search_filter = or_(
            User.email.ilike(f"%{query}%"), User.full_name.ilike(f"%{query}%")
        )

        result = await db.execute(
            select(User)
            .where(search_filter)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(User.email)
        )
        return list(result.scalars().all())

    async def get_superusers(self, db: AsyncSession) -> List[User]:
        """Get all superusers"""
        result = await db.execute(
            select(User)
            .where(User.is_superuser == True)
            .where(User.is_active == True)
            .order_by(User.email)
        )
        return list(result.scalars().all())

    async def email_exists(self, db: AsyncSession, email: str) -> bool:
        """Check if email already exists"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none() is not None

    async def get_users_with_pagination(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_superuser: Optional[bool] = None,
    ) -> List[User]:
        """Get users with advanced filtering"""
        filters = {}
        if is_active is not None:
            filters["is_active"] = is_active
        if is_superuser is not None:
            filters["is_superuser"] = is_superuser

        return await self.get_multi(
            db, skip=skip, limit=limit, filters=filters, order_by="-created_at"
        )
