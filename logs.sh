#!/bin/bash
set -e

BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[INFO]${NC} Tailing logs from all Docker containers..."
docker-compose logs -f
