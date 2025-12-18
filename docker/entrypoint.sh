#!/bin/bash
set -e

echo "🚀 Starting Task Management Backend..."

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL to become available..."
while ! pg_isready -h postgres -p 5432 -U taskuser > /dev/null 2>&1; do
  sleep 1
done
echo "✅ PostgreSQL is ready!"

# Detect if we are in development mode (code mounted via volume)
# If migrations exist in the mounted folder → developer mode → skip auto-migration
if ls /app/alembic/versions/*.py > /dev/null 2>&1; then
    echo "🔍 Developer mode detected (migrations found in mounted volume)"
    echo "ℹ️  Skipping automatic migrations — run 'make migrate' manually when ready"
else
    echo "🆕 Fresh environment detected — applying migrations automatically"
    alembic upgrade head
    echo "✅ Automatic migrations completed"
fi

# Always run seeding — your script is idempotent and safe
echo "🌱 Seeding initial data (idempotent)..."
python scripts/seed_data.py
echo "✅ Seeding completed"

# Start the server
echo "🌐 Starting FastAPI server with reload..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload