from uuid import UUID
from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.base import UUIDModel
from backend.app.models.user import User


class Notification(UUIDModel):
    """Notification model for user alerts."""

    __tablename__ = "notifications"

    type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # task_assigned, comment_added, task_completed, etc.
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    link: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )  # Link to relevant resource
    read: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification {self.title}>"
