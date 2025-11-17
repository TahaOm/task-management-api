#!/bin/bash

# Task Management API - Startup Script
# This script automatically builds and starts all Docker containers

set -e  # Exit on error

echo "🚀 Task Management API - Starting..."
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists, if not copy from example
if [ ! -f "backend/.env" ]; then
    print_warning ".env file not found. Creating from .env.example..."
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        print_success ".env file created. Please update it with your settings."
    else
        print_error ".env.example not found!"
        exit 1
    fi
fi

# Stop any running containers
print_status "Stopping any existing containers..."
docker-compose down 2>/dev/null || true

# Build all images
print_status "Building Docker images..."
docker-compose build --no-cache

print_success "Docker images built successfully!"
echo ""

# Start all services
print_status "Starting all services..."
docker-compose up -d

echo ""
print_success "All services started!"
echo ""

# Wait for services to be healthy
print_status "Waiting for services to be ready..."
echo ""

# Wait for PostgreSQL
print_status "Waiting for PostgreSQL..."
timeout=60
counter=0
until docker-compose exec -T postgres pg_isready -U taskuser -d taskdb > /dev/null 2>&1; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $timeout ]; then
        print_error "PostgreSQL failed to start within $timeout seconds"
        exit 1
    fi
done
print_success "PostgreSQL is ready!"

# Wait for Redis
print_status "Waiting for Redis..."
counter=0
until docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $timeout ]; then
        print_error "Redis failed to start within $timeout seconds"
        exit 1
    fi
done
print_success "Redis is ready!"

# Wait for backend API
print_status "Waiting for Backend API..."
counter=0
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    sleep 2
    counter=$((counter + 2))
    if [ $counter -ge $timeout ]; then
        print_error "Backend API failed to start within $timeout seconds"
        print_status "Checking logs..."
        docker-compose logs backend
        exit 1
    fi
done
print_success "Backend API is ready!"

echo ""

# Run database migrations
print_status "Running database migrations..."
docker-compose exec -T backend alembic upgrade head
print_success "Migrations completed!"

echo ""
echo "======================================"
print_success "🎉 Task Management API is running!"
echo "======================================"
echo ""
echo "📍 Service URLs:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • API ReDoc:         http://localhost:8000/redoc"
echo "   • API Health:        http://localhost:8000/health"
echo "   • Flower (Celery):   http://localhost:5555"
echo ""
echo "🗄️  Database:"
echo "   • PostgreSQL:        localhost:5432"
echo "   • Redis:             localhost:6379"
echo ""
echo "📋 Useful Commands:"
echo "   • View logs:         docker-compose logs -f"
echo "   • Stop services:     docker-compose down"
echo "   • Restart:           ./start.sh"
echo "   • Run migrations:    docker-compose exec backend alembic upgrade head"
echo "   • Database shell:    docker-compose exec postgres psql -U taskuser -d taskdb"
echo "   • Redis shell:       docker-compose exec redis redis-cli"
echo ""
echo "💡 Tips:"
echo "   • Check service status: docker-compose ps"
echo "   • View backend logs:    docker-compose logs -f backend"
echo "   • Seed test data:       docker-compose exec backend python scripts/seed_data.py"
echo ""
print_success "Ready to develop! 🚀"