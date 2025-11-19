"""
Smart database initialization script.
Checks if database is empty before creating tables.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import engine, Base, SessionLocal
from app.models import User  # Import your models to register them
from sqlalchemy import inspect


def is_database_empty() -> bool:
    """Check if database has any tables (is empty)."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return len(tables) == 0


def has_users() -> bool:
    """Check if users table has any data."""
    try:
        db = SessionLocal()
        user_count = db.query(User).count()
        db.close()
        return user_count > 0
    except:
        return False


def init_db():
    """Initialize database only if empty."""
    print("🔧 Checking database state...")

    if is_database_empty():
        print("📦 Database is empty. Creating tables...")
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully!")

            print("\n📊 Created tables:")
            for table_name in Base.metadata.tables.keys():
                print(f"  - {table_name}")

        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            sys.exit(1)
    else:
        print("✅ Database already has tables. Skipping creation.")

        # Check if we have data
        if not has_users():
            print("📝 Database is empty of data - ready for seeding.")
        else:
            print("📊 Database contains data - safe to use.")


if __name__ == "__main__":
    init_db()
