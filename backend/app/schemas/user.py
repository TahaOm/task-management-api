from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    full_name: Optional[str] = None


# Schema for creating a new user
class UserCreate(UserBase):
    """Schema for user registration."""

    password: str  # Plain password (will be hashed)


# Schema for updating user
class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


# Schema for password update
class UserPasswordUpdate(BaseModel):
    """Schema for changing password."""

    old_password: str
    new_password: str


# Schema for user response (what API returns)
class UserResponse(UserBase):
    """Schema for user data returned by API."""

    id: UUID
    avatar_url: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for user in lists (minimal info)
class UserSummary(BaseModel):
    """Minimal user info for lists and references."""

    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
