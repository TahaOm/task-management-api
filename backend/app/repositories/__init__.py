"""
Repository layer for database operations.

Repositories handle all database queries and provide a clean interface
for the service layer. Each repository inherits from BaseRepository
which provides common CRUD operations.

Usage:
    from app.repositories import user_repository

    user = user_repository.get(db, user_id)
    users = user_repository.get_multi(db, skip=0, limit=20)
"""

from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
]
