# 🚀 Quick Start Guide

Get the Task Management API running in 5 minutes!

## Option 1: Docker (Recommended - Fastest)

```bash
# 1. Clone repository
cd task-management-api

# 2. Start all services
docker-compose up -d

# 3. Run migrations
docker-compose exec backend alembic upgrade head

# 4. Access the API
# API: http://localhost:8000/docs
# Flower (Celery Monitor): http://localhost:5555
```

**That's it!** Your API is running with PostgreSQL, Redis, and Celery workers.

---

## Option 2: Local Development (UV)

### Prerequisites
- Python 3.11+
- PostgreSQL running on localhost:5432
- Redis running on localhost:6379

### Setup Steps

```bash
# 1. Navigate to backend
cd task-management-api/backend

# 2. Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Initialize database
uv run python scripts/init_db.py

# 6. Run migrations
uv run alembic revision --autogenerate -m "Initial migration"
uv run alembic upgrade head

# 7. Start the server
uv run uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## What's Running?

After setup, you have:

✅ **FastAPI Backend** - http://localhost:8000
- Interactive API docs at `/docs`
- ReDoc documentation at `/redoc`
- Health check at `/health`

✅ **PostgreSQL Database** - localhost:5432
- Database: `taskdb`
- User: `taskuser`
- Password: `taskpass`

✅ **Redis Cache** - localhost:6379

✅ **Celery Worker** - Background task processor

✅ **Flower** (Docker only) - http://localhost:5555
- Celery task monitoring dashboard

---

## Verify Setup

### Check API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### Check Database Connection
```bash
# If using Docker
docker-compose exec postgres psql -U taskuser -d taskdb -c "\dt"

# If using local PostgreSQL
psql -U taskuser -d taskdb -c "\dt"
```

You should see tables: `users`, `projects`, `tasks`, `comments`, `notifications`, etc.

### Check Redis Connection
```bash
# If using Docker
docker-compose exec redis redis-cli ping

# If using local Redis
redis-cli ping
```

Expected response: `PONG`

---

## Common Commands

### Docker

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Access database
docker-compose exec postgres psql -U taskuser -d taskdb

# Access Redis CLI
docker-compose exec redis redis-cli
```

### UV (Local)

```bash
# Start development server
uv run uvicorn app.main:app --reload

# Run migrations
uv run alembic upgrade head

# Create migration
uv run alembic revision --autogenerate -m "description"

# Run tests
uv run pytest

# Run Celery worker (separate terminal)
uv run celery -A app.tasks.celery_app worker --loglevel=info

# Format code
uv run black app/

# Lint code
uv run ruff check app/
```

---

## Test the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Get API info
curl http://localhost:8000/
```

### Using Python requests

```python
import requests

# Test health endpoint
response = requests.get("http://localhost:8000/health")
print(response.json())
```

### Using the Swagger UI

1. Go to http://localhost:8000/docs
2. Try the `/health` endpoint
3. Explore the auto-generated API documentation

---

## Next Steps

Now that your backend is running:

1. ✅ Setup complete
2. 🔜 Implement authentication endpoints (`app/api/v1/auth.py`)
3. 🔜 Create project CRUD endpoints (`app/api/v1/projects.py`)
4. 🔜 Add task management endpoints (`app/api/v1/tasks.py`)
5. 🔜 Setup WebSocket for real-time updates
6. 🔜 Write tests
7. 🔜 Build the Next.js frontend

---

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors:

```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>

# Or change the port in docker-compose.yml or uvicorn command
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker-compose ps postgres
# Or for local: pg_isready

# Check database credentials in .env match your setup
```

### Migrations Not Working

```bash
# Reset migrations (WARNING: deletes all data)
uv run alembic downgrade base
uv run alembic upgrade head

# Or with Docker
docker-compose exec backend alembic downgrade base
docker-compose exec backend alembic upgrade head
```

### Redis Connection Failed

```bash
# Check Redis is running
docker-compose ps redis
# Or for local: redis-cli ping

# Check REDIS_URL in .env
```

---

## Environment Variables Reference

Key variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Redis
REDIS_URL=redis://host:port/db

# JWT Secret (IMPORTANT: Change in production!)
SECRET_KEY=your-secret-key-min-32-chars

# Celery
CELERY_BROKER_URL=redis://host:port/1
CELERY_RESULT_BACKEND=redis://host:port/2

# Email (optional for now)
SENDGRID_API_KEY=
FROM_EMAIL=noreply@example.com

# CORS
FRONTEND_URL=http://localhost:3000
```

---

## Getting Help

If you're stuck:

1. Check the logs: `docker-compose logs -f` or console output
2. Verify all services are running: `docker-compose ps`
3. Check environment variables are set correctly
4. Ensure PostgreSQL and Redis are accessible
5. Review the full README.md for detailed documentation

---

## You're Ready! 🎉

Your backend is now set up and running. You can:
- Access the API at http://localhost:8000
- View documentation at http://localhost:8000/docs
- Start building the authentication endpoints

Next: Let's implement the authentication system! 🔐