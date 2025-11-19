.PHONY: help up down restart logs

# Default help
help:
	@echo "Task Management API - Makefile commands"
	@echo ""
	@echo "Development & Docker:"
	@echo "  make up        → Start all services (start.sh)"
	@echo "  make down      → Stop all services (stop.sh)"
	@echo "  make restart   → Restart all services (restart.sh)"
	@echo "  make logs      → Tail logs from all containers (logs.sh)"
	@echo ""
	@echo "Usage:"
	@echo "  make <command>"

# Start all services (build + run + init DB + seed)
up:
	@chmod +x start.sh
	@./start.sh

# Stop all services
down:
	@chmod +x stop.sh
	@./stop.sh

# Restart all services
restart:
	@chmod +x restart.sh
	@./restart.sh

# Tail logs
logs:
	@chmod +x logs.sh
	@./logs.sh
