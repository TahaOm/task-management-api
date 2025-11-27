from app.models.baseModel import Base

"""
Database models for the Task Management API.

Import all models here so they're available when importing from app.models
and so Alembic can detect them for migrations.
"""

from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.task import Task
from app.models.comment import Comment
from app.models.notification import Notification

__all__ = [
    "User",
    "Project",
    "ProjectMember",
    "Task",
    "Comment",
    "Notification",
]
