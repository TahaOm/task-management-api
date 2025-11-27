"""
Pydantic schemas for request/response validation.

These schemas define the structure of data sent to and from the API.
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
    UserSummary,
)

from app.schemas.token import (
    Token,
    TokenData,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RevokeTokenRequest,
)

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    LogoutRequest,
    LogoutResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChangeRequest,
    VerifyTokenResponse,
)

from app.schemas.project import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectWithOwner,
    ProjectWithStats,
    ProjectSummary,
    ProjectMemberBase,
    ProjectMemberCreate,
    ProjectMemberUpdate,
    ProjectMemberResponse,
    ProjectMemberWithUser,
)

from app.schemas.task import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskPositionUpdate,
    TaskResponse,
    TaskWithRelations,
    TaskWithStats,
    TaskSummary,
    TaskFilters,
)

from app.schemas.comment import (
    CommentBase,
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentWithUser,
)

from app.schemas.notification import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
    NotificationBulkUpdate,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPasswordUpdate",
    "UserResponse",
    "UserSummary",
    # Token schemas
    "Token",
    "TokenData",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "RevokeTokenRequest",
    # Auth schemas
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "LogoutRequest",
    "LogoutResponse",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "PasswordChangeRequest",
    "VerifyTokenResponse",
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectWithOwner",
    "ProjectWithStats",
    "ProjectSummary",
    "ProjectMemberBase",
    "ProjectMemberCreate",
    "ProjectMemberUpdate",
    "ProjectMemberResponse",
    "ProjectMemberWithUser",
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskPositionUpdate",
    "TaskResponse",
    "TaskWithRelations",
    "TaskWithStats",
    "TaskSummary",
    "TaskFilters",
    # Comment schemas
    "CommentBase",
    "CommentCreate",
    "CommentUpdate",
    "CommentResponse",
    "CommentWithUser",
    # Notification schemas
    "NotificationBase",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
    "NotificationBulkUpdate",
]
