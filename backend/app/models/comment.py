# app/models/comment.py
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from backend.app.db.base import UUIDModel
from app.models import Task, User


class Comment(UUIDModel):  # Inherit from UUIDModel instead of Base
    """Comment model for task discussions."""

    __tablename__ = "comments"

    # No need for id, created_at, updated_at - they come from UUIDModel
    content: Mapped[str] = mapped_column(Text, nullable=False)

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment on Task {self.task_id}>"
