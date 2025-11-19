from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class User(Base):
    """User model for authentication and user management."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    # owned_projects = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    # project_memberships = relationship("ProjectMember", back_populates="user", cascade="all, delete-orphan")
    # created_tasks = relationship("Task", back_populates="creator", foreign_keys="Task.creator_id")
    # assigned_tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assignee_id")
    # comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    # notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
