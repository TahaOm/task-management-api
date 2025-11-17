.PHONY: help install dev test clean migrate migration db-init docker-up docker-down format lint

# Default target
help:
	@echo "Task Management API - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install       Install dependencies with UV"
	@echo "  make db-init       Initialize database tables"
	@echo "  make migration     Create new Alembic migration"
	@echo "  make migrate       Apply pending migrations"
	@echo ""
	@echo "Development:"
	@echo "  make dev           Start development server"
	@echo "  make worker        Start Celery worker"
	@echo "  make test          Run tests"
	@echo "  make format        Format code with Black"
	@echo "  make lint          Lint code with Ruff"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     Start all Docker services"
	@echo "  make docker-down   Stop all Docker services"
	@echo "  make docker-logs   View Docker logs"
	@echo "  make docker-shell  Open shell in backend container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         Remove cache and temporary files"

# Setup & Installation
install:
	@echo "📦 Installing dependencies with UV..."
	cd backend && uv sync

db-init:
	@echo "🔧 Initializing database..."
	cd backend && uv run python scripts/init_db.py

migration:
	@echo "📝 Creating new migration..."
	@read -p "Enter migration message: " msg; \
	cd backend && uv run alembic revision --autogenerate -m "$$msg"

migrate:
	@echo "⬆️  Applying migrations..."
	cd backend && uv run alembic upgrade head

# Development
dev:
	@echo "🚀 Starting development server..."
	cd backend && uv run uvicorn app.main:app --reload --port 8000

worker:
	@echo "⚙️  Starting Celery worker..."
	cd backend && uv run celery -A app.tasks.celery_app worker --loglevel=info

test:
	@echo "🧪 Running tests..."
	cd backend && uv run pytest -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	cd backend && uv run pytest --cov=app --cov-report=html --cov-report=term

format:
	@echo "✨ Formatting code..."
	cd backend && uv run black app/ tests/

lint:
	@echo "🔍 Linting code..."
	cd backend && uv run ruff check app/ tests/

# Docker
docker-up:
	@echo "🐳 Starting Docker services..."
	@chmod +x start.sh
	@./start.sh

docker-down:
	@echo "🛑 Stopping Docker services..."
	@chmod +x stop.sh
	@./stop.sh

docker-restart:
	@echo "🔄 Restarting Docker services..."
	@chmod +x restart.sh
	@./restart.sh

docker-build:
	@echo "🏗️  Building Docker images..."
	docker-compose build --no-cache

docker-logs:
	@echo "📋 Viewing Docker logs..."
	docker-compose logs -f

docker-shell:
	@echo "🐚 Opening shell in backend container..."
	docker-compose exec backend /bin/bash

docker-migrate:
	@echo "⬆️  Running migrations in Docker..."
	docker-compose exec backend alembic upgrade head

docker-migration:
	@echo "📝 Creating migration in Docker..."
	@read -p "Enter migration message: " msg; \
	docker-compose exec backend alembic revision --autogenerate -m "$$msg"

# Database
db-shell:
	@echo "💾 Opening PostgreSQL shell..."
	docker-compose exec postgres psql -U taskuser -d taskdb

db-reset:
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		cd backend && uv run alembic downgrade base && uv run alembic upgrade head; \
		echo "✅ Database reset complete"; \
	else \
		echo "❌ Cancelled"; \
	fi

redis-shell:
	@echo "🔴 Opening Redis CLI..."
	docker-compose exec redis redis-cli

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "✅ Cleanup complete"

# Seed data
seed:
	@echo "🌱 Seeding database with test data..."
	cd backend && uv run python scripts/seed_data.py

# Production build
build:
	@echo "🏗️  Building Docker images..."
	docker-compose build

# Complete setup
setup: install db-init migrate
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Start services: make docker-up"
	@echo "  2. Or run locally: make dev"
	@echo "  3. Visit: http://localhost:8000/docs"