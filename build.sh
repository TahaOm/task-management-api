# build.sh
#!/bin/bash
set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}[INFO]${NC} Building Docker images..."
docker-compose build --no-cache
echo -e "${GREEN}[SUCCESS]${NC} Images built. Run './start.sh' to start services."