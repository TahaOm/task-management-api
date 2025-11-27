from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserSummary


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    task_id: UUID


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class CommentWithUser(CommentResponse):
    user: "UserSummary"
