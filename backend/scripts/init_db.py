"""
Database initialization script.

This script creates all database tables based on SQLAlchemy models.
Run this before running Alembic migrations.

Usage:
    uv run python scripts/init_db.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import engine, Base
from app.models import User  # , Project, ProjectMember, Task, Comment, Notification


def init_db():
    """Initialize database by creating all tables."""
    print("🔧 Creating database tables...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")

        print("\n📝 Next steps:")
        print("  1. Run: uv run alembic revision --autogenerate -m 'Initial migration'")
        print("  2. Run: uv run alembic upgrade head")
        print("  3. (Optional) Run: uv run python scripts/seed_data.py")

    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_db()
