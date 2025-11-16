FROM postgres:15-alpine

# Set environment variables with defaults
ENV POSTGRES_USER=taskuser
ENV POSTGRES_PASSWORD=taskpass
ENV POSTGRES_DB=taskdb

# Install additional extensions
RUN apk add --no-cache postgresql-contrib

# Create custom initialization script
COPY init-db.sh /docker-entrypoint-initdb.d/

# Set proper permissions
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Expose PostgreSQL port
EXPOSE 5432

# Add health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# Set up data directory
VOLUME /var/lib/postgresql/data