#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

print_status "🚀 Starting Task Management System..."

docker-compose up -d

print_status "Waiting for services to initialize..."
sleep 10

until curl -f http://localhost:8000/health > /dev/null 2>&1; do
  sleep 2
done

print_success "🎉 System is ready!"
print_warning "ℹ️  Developer tip: Create models → 'make migration' → 'make migrate'"

echo ""
echo "📚 API Docs:      http://localhost:8000/docs"
echo "🌐 Frontend:      http://localhost:3000"
echo "📊 pgAdmin:       http://localhost:8080"
echo "🌺 Flower:        http://localhost:5555"
echo ""