#!/bin/bash
# Modern migration script using Alembic
# This replaces the old run_migration.sh

set -e

echo "🔄 Running Database Migrations with Alembic"
echo "==========================================="

# Check if running in Docker or local
if [ -f "/.dockerenv" ]; then
    echo "📦 Running in Docker container"
    cd /app
else
    echo "💻 Running locally"
    cd "$(dirname "$0")/.."
fi

# Activate virtual environment if it exists (local only)
if [ -d "venv" ] && [ ! -f "/.dockerenv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
fi

# Run Alembic migrations
echo ""
echo "⬆️  Upgrading database to latest version..."
alembic upgrade head

echo ""
echo "✅ Migrations completed successfully!"
echo ""

# Show current migration status
echo "📊 Current Migration Status:"
alembic current

echo ""
echo "==========================================="
