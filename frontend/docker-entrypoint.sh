#!/bin/sh
set -e

echo "Setting up .next directory..."
rm -rf /app/.next
mkdir -p /app/.next
chmod -R 777 /app/.next

exec "$@"
