from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expires


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    token_type: Optional[str] = "access"  # access or refresh
    exp: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RevokeTokenRequest(BaseModel):
    token: str  # can be access or refresh token
    token_type_hint: Optional[str] = Field(
        None, pattern="^(access_token|refresh_token)$"
    )
