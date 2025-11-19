.PHONY: help up down restart logs build clean

help:
	@echo "Task Management API - Makefile commands"
	@echo ""
	@echo "Development:"
	@echo "  make up        → Start services (no rebuild, keeps data)"
	@echo "  make down      → Stop services (keeps data)"
	@echo "  make restart   → Restart services (keeps data)"
	@echo "  make logs      → Tail logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make build     → Build/rebuild images"
	@echo "  make clean     → 🚨 STOP AND DELETE ALL DATA (docker-compose down -v)"
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

# Maintenance
build:
	@chmod +x build.sh
	@./build.sh

clean:
	@echo "🚨 WARNING: This will delete ALL database data!"
	@echo "    Postgres data, Redis data - everything will be lost!"
	@read -p "    Are you sure? (y/N): " confirm && [ $$confirm = y ] || exit 1
	docker-compose down -v
	@echo "🧹 All containers and volumes removed. Data deleted!"