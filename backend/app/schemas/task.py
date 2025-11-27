from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.project import ProjectSummary
from app.schemas.user import UserSummary


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: str = Field(default="todo", pattern="^(todo|in_progress|review|done)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    project_id: UUID
    assignee_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(todo|in_progress|review|done)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    assignee_id: Optional[UUID] = None
    due_date: Optional[datetime] = None


class TaskPositionUpdate(BaseModel):
    position: int = Field(..., ge=0)
    status: Optional[str] = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    creator_id: UUID
    assignee_id: Optional[UUID] = None
    position: int
    created_at: datetime
    updated_at: datetime


class TaskWithRelations(TaskResponse):
    creator: "UserSummary"
    assignee: Optional["UserSummary"] = None
    project: ProjectSummary


class TaskWithStats(TaskWithRelations):
    comments_count: int = 0


class TaskSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    status: str
    priority: str


class TaskFilters(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    search: Optional[str] = None
