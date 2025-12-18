# scripts/seed_data.py
"""
Seed initial data into the database.
"""

import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import uuid


async def create_superuser():
    """Create a default superuser."""
    async with SessionLocal() as session:
        # Check if superuser already exists
        from sqlalchemy import select

        result = await session.execute(
            select(User).where(User.email == "admin@example.com")
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("✅ Superuser already exists")
            return existing_user

        # Create new superuser
        superuser = User(
            email="admin@example.com",
            hashed_password=get_password_hash("Admin123!"),
            full_name="System Administrator",
            is_superuser=True,
            is_active=True,
        )

        session.add(superuser)
        await session.commit()
        await session.refresh(superuser)

        print(f"✅ Superuser created: {superuser.email}")
        return superuser


async def create_test_users():
    """Create test users."""
    async with SessionLocal() as session:
        test_users = [
            {
                "email": "manager@example.com",
                "password": "Manager123!",
                "full_name": "Project Manager",
                "is_superuser": False,
            },
            {
                "email": "developer@example.com",
                "password": "Developer123!",
                "full_name": "Software Developer",
                "is_superuser": False,
            },
            {
                "email": "designer@example.com",
                "password": "Designer123!",
                "full_name": "UI/UX Designer",
                "is_superuser": False,
            },
        ]

        created_users = []
        for user_data in test_users:
            # Check if user exists
            from sqlalchemy import select

            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"✅ User already exists: {user_data['email']}")
                created_users.append(existing_user)
                continue

            # Create new user
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                full_name=user_data["full_name"],
                is_superuser=user_data["is_superuser"],
                is_active=True,
            )

            session.add(user)
            created_users.append(user)
            print(f"✅ User created: {user_data['email']}")

        await session.commit()

        # Refresh all users
        for user in created_users:
            await session.refresh(user)

        return created_users


async def main():
    """Main seeding function."""
    print("🌱 Seeding initial data...")

    try:
        # Create superuser
        admin = await create_superuser()

        # Create test users
        users = await create_test_users()

        print(f"\n🎉 Seeding complete!")
        print(f"📊 Created {len(users) + 1} users total")
        print(f"🔑 Admin credentials: admin@example.com / Admin123!")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
