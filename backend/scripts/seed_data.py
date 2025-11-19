# """
# Database seeding script.
# Populates database with demo data for development.
# """

# import sys
# from pathlib import Path
# from datetime import datetime, timedelta

# sys.path.append(str(Path(__file__).resolve().parents[1]))

# from app.database import SessionLocal
# from app.models import User, Project, Task, Comment
# from app.core.security import get_password_hash

# def seed_data():
#     """Seed database with demo data."""
#     print("🌱 Seeding database with demo data...")

#     db = SessionLocal()

#     try:
#         # Check if we already have data
#         if db.query(User).count() > 0:
#             print("✅ Database already has data. Skipping seeding.")
#             return

#         # Create demo users
#         users = [
#             User(
#                 email="admin@taskapp.com",
#                 hashed_password=get_password_hash("admin123"),
#                 full_name="Admin User",
#                 is_active=True,
#                 is_superuser=True
#             ),
#             User(
#                 email="john@taskapp.com",
#                 hashed_password=get_password_hash("john123"),
#                 full_name="John Doe",
#                 is_active=True
#             ),
#             User(
#                 email="sarah@taskapp.com",
#                 hashed_password=get_password_hash("sarah123"),
#                 full_name="Sarah Wilson",
#                 is_active=True
#             )
#         ]

#         db.add_all(users)
#         db.flush()  # Get IDs

#         # Create projects
#         projects = [
#             Project(
#                 name="Website Redesign",
#                 description="Complete redesign of company website",
#                 owner_id=users[0].id
#             ),
#             Project(
#                 name="Mobile App Development",
#                 description="New task management mobile app",
#                 owner_id=users[1].id
#             )
#         ]

#         db.add_all(projects)
#         db.flush()

#         # Create tasks
#         tasks = [
#             Task(
#                 title="Design Homepage",
#                 description="Create new homepage layout and design",
#                 status="in_progress",
#                 priority="high",
#                 due_date=datetime.now() + timedelta(days=7),
#                 project_id=projects[0].id,
#                 assignee_id=users[1].id,
#                 creator_id=users[0].id
#             ),
#             Task(
#                 title="API Development",
#                 description="Build backend API endpoints",
#                 status="todo",
#                 priority="medium",
#                 due_date=datetime.now() + timedelta(days=14),
#                 project_id=projects[1].id,
#                 assignee_id=users[2].id,
#                 creator_id=users[1].id
#             )
#         ]

#         db.add_all(tasks)
#         db.flush()

#         # Create comments
#         comments = [
#             Comment(
#                 content="Let's use a modern color scheme for this",
#                 task_id=tasks[0].id,
#                 author_id=users[1].id
#             ),
#             Comment(
#                 content="I'll start working on the backend first",
#                 task_id=tasks[1].id,
#                 author_id=users[2].id
#             )
#         ]

#         db.add_all(comments)
#         db.commit()

#         print("✅ Demo data seeded successfully!")
#         print(f"   👥 Users: {len(users)}")
#         print(f"   📁 Projects: {len(projects)}")
#         print(f"   ✅ Tasks: {len(tasks)}")
#         print(f"   💬 Comments: {len(comments)}")

#     except Exception as e:
#         db.rollback()
#         print(f"❌ Error seeding data: {e}")
#         sys.exit(1)
#     finally:
#         db.close()

# if __name__ == "__main__":
#     seed_data()
