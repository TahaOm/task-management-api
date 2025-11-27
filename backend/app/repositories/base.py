from typing import Generic, TypeVar, List, Optional, Any, Dict
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Integer, and_, select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from backend.app.database import Base
from backend.app.models.baseModel import UUIDModel


# Generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=UUIDModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic async repository with CRUD operations for any model.

    This provides common database operations for all models:
    - Create
    - Read (get one, get many)
    - Update
    - Delete
    - Pagination
    - Filtering

    Usage:
        class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
            pass
    """

    def __init__(self, model: type[ModelType]):
        """
        Initialize repository with a SQLAlchemy model.

        Args:
            model: SQLAlchemy model class (e.g., User, Task)
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            db: Database session
            id: Record ID (UUID, int, etc.)

        Returns:
            Model instance or None if not found
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and filtering.

        Args:
            db: Database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            filters: Dictionary of field: value filters
            order_by: Field name to order by (prefix with '-' for DESC)

        Returns:
            List of model instances

        Example:
            users = await repository.get_multi(
                db,
                skip=0,
                limit=20,
                filters={"is_active": True},
                order_by="-created_at"
            )
        """
        query = select(self.model)

        # Apply filters
        if filters:
            filter_clauses = []
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    filter_clauses.append(getattr(self.model, field) == value)
            if filter_clauses:
                query = query.where(and_(*filter_clauses))

        # Apply ordering
        if order_by:
            if order_by.startswith("-"):
                # Descending order
                field_name = order_by[1:]
                if hasattr(self.model, field_name):
                    query = query.order_by(getattr(self.model, field_name).desc())
            else:
                # Ascending order
                if hasattr(self.model, order_by):
                    query = query.order_by(getattr(self.model, order_by))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        scalar_result = result.scalars()
        # Explicitly convert to list
        items = scalar_result.all()
        return list(items)

    async def get_count(
        self,
        db: AsyncSession,
        *,
        filters: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Get count of records matching filters.

        Args:
            db: Database session
            filters: Dictionary of field: value filters

        Returns:
            Count of matching records
        """
        query = select(func.count()).select_from(self.model)

        if filters:
            filter_clauses = []
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    filter_clauses.append(getattr(self.model, field) == value)
            if filter_clauses:
                query = query.where(and_(*filter_clauses))

        result = await db.execute(query)
        return result.scalar_one()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            db: Database session
            obj_in: Pydantic schema with data to create

        Returns:
            Created model instance

        Example:
            user_data = UserCreate(email="test@example.com", password="secret")
            user = await repository.create(db, obj_in=user_data)
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            db: Database session
            db_obj: Existing model instance to update
            obj_in: Pydantic schema or dict with update data

        Returns:
            Updated model instance

        Example:
            user = await repository.get(db, id=user_id)
            update_data = UserUpdate(full_name="New Name")
            updated_user = await repository.update(db, db_obj=user, obj_in=update_data)
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_by_id(
        self,
        db: AsyncSession,
        *,
        id: Any,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> Optional[ModelType]:
        """
        Update a record by ID without needing the object first.

        Args:
            db: Database session
            id: Record ID to update
            obj_in: Pydantic schema or dict with update data

        Returns:
            Updated model instance or None if not found
        """
        db_obj = await self.get(db, id=id)
        if not db_obj:
            return None

        return await self.update(db, db_obj=db_obj, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, id: Any) -> bool:
        """
        Delete a record by ID.

        Args:
            db: Database session
            id: Record ID to delete

        Returns:
            Deleted model instance or None if not found

        Example:
            deleted_user = await repository.delete(db, id=user_id)
        """
        entity = await self.get(db, id=id)
        if not entity:
            return False

        await db.delete(entity)
        await db.commit()
        return True

    async def get_by_field(
        self, db: AsyncSession, field: str, value: Any
    ) -> Optional[ModelType]:
        """
        Get a single record by any field.

        Args:
            db: Database session
            field: Field name to filter by
            value: Value to match

        Returns:
            Model instance or None if not found

        Example:
            user = await repository.get_by_field(db, "email", "test@example.com")
        """
        if hasattr(self.model, field):
            result = await db.execute(
                select(self.model).where(getattr(self.model, field) == value)
            )
            return result.scalar_one_or_none()
        return None

    async def exists(self, db: AsyncSession, id: Any) -> bool:
        """
        Check if a record exists by ID.

        Args:
            db: Database session
            id: Record ID to check

        Returns:
            True if exists, False otherwise
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none() is not None

    async def exists_by_field(self, db: AsyncSession, field: str, value: Any) -> bool:
        """
        Check if a record exists by field value.

        Args:
            db: Database session
            field: Field name to check
            value: Value to match

        Returns:
            True if exists, False otherwise
        """
        if hasattr(self.model, field):
            result = await db.execute(
                select(self.model).where(getattr(self.model, field) == value).limit(1)
            )
            return result.scalar_one_or_none() is not None
        return False

    async def bulk_create(
        self, db: AsyncSession, *, objects_in: List[CreateSchemaType]
    ) -> List[ModelType]:
        """
        Create multiple records at once.

        Args:
            db: Database session
            objects_in: List of Pydantic schemas with data

        Returns:
            List of created model instances
        """
        db_objects = []
        for obj_in in objects_in:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db_objects.append(db_obj)

        db.add_all(db_objects)
        await db.commit()

        # Refresh all objects
        for db_obj in db_objects:
            await db.refresh(db_obj)

        return db_objects

    async def bulk_delete(self, db: AsyncSession, *, ids: List[Any]) -> int:
        """
        Delete multiple records by IDs.

        Args:
            db: Database session
            ids: List of record IDs to delete

        Returns:
            Number of deleted records
        """
        if not ids:
            return 0

        # Get count before delete
        count_query = select(func.count()).where(self.model.id.in_(ids))
        count_result = await db.execute(count_query)
        before_count = count_result.scalar_one() or 0

        if before_count == 0:
            return 0

        # Perform delete
        stmt = delete(self.model).where(self.model.id.in_(ids))
        await db.execute(stmt)
        await db.commit()

        return before_count
