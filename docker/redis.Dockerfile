FROM redis:7-alpine

# Copy custom Redis configuration
COPY redis.conf /usr/local/etc/redis/redis.conf

# Create data directory with proper permissions
RUN mkdir -p /data && chown redis:redis /data

# Switch to non-root redis user (already exists in base image)
USER redis

# Use custom config
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]