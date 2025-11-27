from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class NotificationBase(BaseModel):
    type: str = Field(..., max_length=100)
    title: str = Field(..., max_length=255)
    message: Optional[str] = None
    link: Optional[str] = Field(None, max_length=500)


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationUpdate(BaseModel):
    read: bool


class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    read: bool
    created_at: datetime


class NotificationBulkUpdate(BaseModel):
    notification_ids: List[UUID]
    read: bool
