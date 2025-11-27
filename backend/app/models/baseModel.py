# app/models/base.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func
import uuid
from datetime import datetime
from typing import Any, Optional


# Base class for all models
class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Mixin for created_at and updated_at fields."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class UUIDModel(Base, TimestampMixin):
    """
    Base model with UUID primary key and timestamps.
    All application models should inherit from this.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    __abstract__ = True

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
