from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional
import uuid
from datetime import datetime


class UserBase(BaseModel):
    """Base schema with common user fields."""

    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserResponse(UserBase):
    """Schema for returning user data (without sensitive information)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserPasswordChange(BaseModel):
    """Schema for password change."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile (excludes sensitive fields)."""

    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class Token(BaseModel):
    """Schema for authentication token response."""

    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: Optional[uuid.UUID] = None


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""

    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class UserFilter(BaseModel):
    """Schema for filtering users in queries."""

    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    email: Optional[str] = None
