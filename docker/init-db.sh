#!/bin/bash
set -e

# This script runs when the PostgreSQL container is first created

echo "🔧 Initializing PostgreSQL database..."

# Create extensions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Enable UUID extension for generating UUIDs
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Enable pg_trgm for text search optimization
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    
    -- Enable btree_gist for advanced indexing
    CREATE EXTENSION IF NOT EXISTS "btree_gist";
    
    -- Log success
    SELECT 'PostgreSQL initialization complete!' as status;
EOSQL

echo "✅ PostgreSQL database initialized successfully!"
echo "📊 Database: $POSTGRES_DB"
echo "👤 User: $POSTGRES_USER"
echo "🔌 Ready to accept connections on port 5432"