from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)


class RegisterResponse(BaseModel):
    message: str
    user: "UserResponse"


class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None  # if provided, revoke this specific token


class LogoutResponse(BaseModel):
    message: str = "Successfully logged out"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class VerifyTokenResponse(BaseModel):
    valid: bool
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None
