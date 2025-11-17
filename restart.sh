#!/bin/bash

# Task Management API - Restart Script
# This script restarts all Docker containers

set -e

echo "🔄 Restarting Task Management API..."
echo ""

# Stop services
./stop.sh

echo ""
echo "⏳ Waiting 3 seconds before restart..."
sleep 3
echo ""

# Start services
./start.sh