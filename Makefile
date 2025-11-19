.PHONY: help up down restart logs build clean migration migrate downgrade reset-db

help:
	@echo "Task Management API - Makefile commands"
	@echo ""
	@echo "Development:"
	@echo "  make up        → Start services (no rebuild, keeps data)"
	@echo "  make down      → Stop services (keeps data)"
	@echo "  make restart   → Restart services (keeps data)"
	@echo "  make logs      → Tail logs"
	@echo ""
	@echo "Database & Migrations:"
	@echo "  make migration → Create new migration with message"
	@echo "  make migrate   → Run all pending migrations"
	@echo "  make downgrade → Rollback last migration"
	@echo "  make reset-db  → Reset database (WARNING: deletes data)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make build     → Build/rebuild images"
	@echo "  make clean     → 🚨 STOP AND DELETE ALL DATA (nuclear option)"
	@echo ""
	@echo "Usage:"
	@echo "  make <command>"

# Development (data-safe)
up:
	@chmod +x start.sh
	@./start.sh

down:
	@chmod +x stop.sh
	@./stop.sh

restart:
	@chmod +x restart.sh
	@./restart.sh

logs:
	@chmod +x logs.sh
	@./logs.sh

# Database & Migrations
migration:
	@echo "📝 Creating new migration..."
	@read -p "Enter migration message: " message; \
	docker-compose exec backend alembic revision --autogenerate -m "$$message"

migrate:
	@echo "🔄 Running migrations..."
	docker-compose exec backend alembic upgrade head

downgrade:
	@echo "↩️  Rolling back last migration..."
	docker-compose exec backend alembic downgrade -1

reset-db:
	@echo "🔄 Resetting database..."
	@echo "⚠️  This will delete all data and recreate tables!"
	@read -p "Are you sure? (y/N): " confirm && [ $$confirm = y ] || exit 1
	docker-compose exec backend python scripts/init_db.py
	# docker-compose exec backend python scripts/seed_data.py  # COMMENTED - tables don't exist yet

# Maintenance
build:
	@chmod +x build.sh
	@./build.sh

clean:
	@echo "🚨 NUCLEAR OPTION: This will delete ALL database data!"
	@echo "    Postgres data, Redis data - everything will be lost!"
	@read -p "    Are you sure? (y/N): " confirm && [ $$confirm = y ] || exit 1
	docker-compose down -v
	@echo "🧹 All containers and volumes removed. Data deleted!"