.PHONY: help up down restart logs build clean migration migrate downgrade reset-db seed reseed full-reset

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
	@echo "  make migrate    → Apply all pending migrations"
	@echo "  make downgrade  → Rollback last migration"
	@echo "  make reset-db   → Full database reset (downgrade + upgrade)"
	@echo "  make seed       → Run seeding script (creates admin/test users)"
	@echo "  make reseed     → Reset DB schema + seed fresh data"
	@echo "  make full-reset → 🚨 NUCLEAR: Delete ALL volumes + reset DB + seed"
	@echo ""
	@echo "Maintenance:"
	@echo "  make build      → Build/rebuild Docker images"
	@echo "  make clean      → 🚨 Stop + delete ALL data/volumes (same as full-reset but no reseed)"
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
	@echo "🔄 Applying pending migrations..."
	docker-compose exec backend alembic upgrade head

downgrade:
	@echo "↩️  Rolling back last migration..."
	docker-compose exec backend alembic downgrade -1

reset-db:
	@echo "⚠️  WARNING: This will DROP ALL TABLES and recreate them via migrations!"
	@echo "    All existing data will be lost."
	@read -p "    Type 'yes' to confirm: " confirm && [ $$confirm = 'yes' ] || (echo "❌ Aborted."; exit 1)
	@echo "🔄 Downgrading to base..."
	docker-compose exec backend alembic downgrade base
	@echo "🔄 Upgrading to head..."
	docker-compose exec backend alembic upgrade head
	@echo "✅ Database fully reset (schema recreated)"

seed:
	@echo "🌱 Running data seeding (admin + test users)..."
	docker-compose exec backend python scripts/seed_data.py
	@echo "✅ Seeding complete!"

reseed: reset-db seed
	@echo "🔥 Database schema reset and freshly seeded!"

full-reset: clean reseed
	@echo "💥 FULL NUCLEAR RESET COMPLETE!"
	@echo "    → All volumes deleted"
	@echo "    → Database schema rebuilt"
	@echo "    → Fresh admin + test users created"
	@echo ""
	@echo "🚀 Now run: make up"

# Maintenance
build:
	@chmod +x build.sh
	@./build.sh

clean:
	@echo "🚨 NUCLEAR OPTION: This will delete ALL containers and volumes!"
	@echo "    PostgreSQL data, Redis data — everything will be gone."
	@read -p "    Type 'yes' to confirm: " confirm && [ $$confirm = 'yes' ] || (echo "❌ Aborted."; exit 1)
	docker-compose down -v
	@echo "🧹 Cleanup complete — all data deleted!"