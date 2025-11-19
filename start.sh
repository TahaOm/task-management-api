#!/bin/bash

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
print_status "🚀 Starting Task Management API (All-in-One)..."

# Check Docker
if ! command -v docker &> /dev/null; then print_error "Docker not installed."; exit 1; fi
if ! command -v docker-compose &> /dev/null; then print_error "Docker Compose not installed."; exit 1; fi

# Build & up
print_status "Building Docker images..."
docker-compose build --no-cache
print_status "Starting Docker services..."
docker-compose up -d

# Wait for PostgreSQL
print_status "Waiting for PostgreSQL..."
timeout=60; counter=0
until docker-compose exec -T postgres pg_isready -U taskuser -d taskdb > /dev/null 2>&1; do
    sleep 1; counter=$((counter+1))
    if [ $counter -ge $timeout ]; then print_error "PostgreSQL failed to start"; exit 1; fi
done
print_success "PostgreSQL ready!"

# Wait for Redis
print_status "Waiting for Redis..."
counter=0
until docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; do
    sleep 1; counter=$((counter+1))
    if [ $counter -ge $timeout ]; then print_error "Redis failed to start"; exit 1; fi
done
print_success "Redis ready!"

# Wait for backend
print_status "Waiting for backend API..."
counter=0
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    sleep 2; counter=$((counter+2))
    if [ $counter -ge $timeout ]; then print_error "Backend failed to start"; docker-compose logs backend; exit 1; fi
done
print_success "Backend API ready!"

# Run migrations
print_status "Running database migrations..."
docker-compose exec -T backend alembic upgrade head
print_success "Migrations complete!"

# Init DB tables
print_status "Initializing database tables..."
docker-compose exec -T backend python scripts/init_db.py
print_success "Database initialization complete!"

# Seed test/demo data
print_status "Seeding database with demo data..."
docker-compose exec -T backend python scripts/seed_data.py
print_success "Database seeding complete!"

echo ""
print_success "🎉 All services ready for development!"
echo "API Docs: http://localhost:8000/docs"
echo "Flower:   http://localhost:5555"
echo "Postgres: localhost:5432"
echo "Redis:    localhost:6379"
echo ""
