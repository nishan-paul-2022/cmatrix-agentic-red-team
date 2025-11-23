#!/bin/sh
set -e

# Fix permissions for .next directory
mkdir -p /app/.next
chmod -R 777 /app/.next 2>/dev/null || true

# Execute the main command
exec "$@"
