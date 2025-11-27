from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Task(Base):
    """Task model for individual work items."""

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="todo", nullable=False, index=True)
    priority = Column(String(50), default="medium", nullable=False, index=True)
    position = Column(Integer, default=0, nullable=False)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    creator_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
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
    project = relationship("Project", back_populates="tasks")
    creator = relationship(
        "User", back_populates="created_tasks", foreign_keys=[creator_id]
    )
    assignee = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_id]
    )
    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Task {self.title}>"
