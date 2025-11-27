from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str | Any, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token with timezone-aware datetime.

    Args:
        subject: The subject of the token (usually user ID)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    secret_key = settings.SECRET_KEY
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured")

    # Use timezone-aware UTC datetime
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "iat": datetime.now(timezone.utc),  # Issued at
    }

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: str | Any, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token with timezone-aware datetime.

    Args:
        subject: The subject of the token (usually user ID)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT refresh token
    """
    secret_key = settings.SECRET_KEY
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured")

    # Use timezone-aware UTC datetime
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),  # Issued at
    }

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode JWT token.

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload or None if invalid
    """
    secret_key = settings.SECRET_KEY
    if not secret_key:
        raise ValueError("SECRET_KEY is not configured")

    try:
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token

    Returns:
        User ID or None if token is invalid
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "access":
        return payload.get("sub")
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if token is expired.

    Args:
        token: JWT token to check

    Returns:
        True if expired, False otherwise
    """
    payload = verify_token(token)
    if not payload:
        return True

    exp_timestamp = payload.get("exp")
    if not exp_timestamp:
        return True

    # Compare with current UTC time
    exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    return datetime.now(timezone.utc) >= exp_datetime


def create_tokens_pair(user_id: str | Any) -> dict[str, str]:
    """
    Create both access and refresh tokens.

    Args:
        user_id: User identifier

    Returns:
        Dictionary with access_token and refresh_token
    """
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Create new access token using valid refresh token.

    Args:
        refresh_token: Valid refresh token

    Returns:
        New access token or None if refresh token is invalid
    """
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    return create_access_token(subject=user_id)


# Password strength validation
def validate_password_strength(password: str) -> dict[str, bool | str]:
    """
    Validate password strength.

    Args:
        password: Password to validate

    Returns:
        Dictionary with validation results
    """
    if len(password) < 8:
        return {
            "valid": False,
            "message": "Password must be at least 8 characters long",
        }

    if not any(c.isupper() for c in password):
        return {
            "valid": False,
            "message": "Password must contain at least one uppercase letter",
        }

    if not any(c.islower() for c in password):
        return {
            "valid": False,
            "message": "Password must contain at least one lowercase letter",
        }

    if not any(c.isdigit() for c in password):
        return {"valid": False, "message": "Password must contain at least one digit"}

    return {"valid": True, "message": "Password meets strength requirements"}


# Security headers utilities
def get_security_headers() -> dict[str, str]:
    """
    Get common security headers for responses.

    Returns:
        Dictionary of security headers
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
