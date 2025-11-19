#!/bin/bash
set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

print_status "Restarting all services..."
./stop.sh
./start.sh
print_success "Services restarted successfully!"
