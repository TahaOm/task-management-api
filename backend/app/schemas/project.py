from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.user import UserSummary


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="active", pattern="^(active|archived)$")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(active|archived)$")


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime


class ProjectWithOwner(ProjectResponse):
    owner: "UserSummary"  # Forward reference


class ProjectWithStats(ProjectResponse):
    total_tasks: int = 0
    completed_tasks: int = 0
    members_count: int = 0


class ProjectSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    status: str


# Project Member Schemas
class ProjectMemberBase(BaseModel):
    role: str = Field(default="member", pattern="^(owner|admin|member)$")


class ProjectMemberCreate(ProjectMemberBase):
    user_id: UUID
    project_id: UUID


class ProjectMemberUpdate(BaseModel):
    role: Optional[str] = Field(None, pattern="^(owner|admin|member)$")


class ProjectMemberResponse(ProjectMemberBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    user_id: UUID
    joined_at: datetime


class ProjectMemberWithUser(ProjectMemberResponse):
    user: "UserSummary"
