#!/bin/bash
set -e

# Load environment variables if .env exists
if [ -f .env ]; then
  # Use a more robust way to export variables from .env
  set -a
  source .env
  set +a
fi

echo "🚀 Starting Automated Database Migration..."

# Ensure we're in the right directory
cd "$(dirname "$0")/.."

# 1. Run migrations first (ensure database matches the latest version)
if [ "$DEBUG" = "true" ] || [ "$MODE" = "development" ]; then
  echo "🔍 Development Mode: Checking for model changes..."
  
  # Generate a unique revision ID
  REV_ID="auto_$(date +%Y%m%d_%H%M%S)"
  
  # Auto-generate a migration if models have changed
  # We capture the output to determine if changes were actually found
  set +e
  REVISION_OUTPUT=$(alembic revision --autogenerate -m "auto_migration" --rev-id "$REV_ID" 2>&1)
  REVISION_EXIT_CODE=$?
  set -e
  
  if echo "$REVISION_OUTPUT" | grep -q "No changes detected"; then
    echo "✅ No model changes detected. Database is up-to-date."
    # If a file was somehow created (unlikely with this output), it's not needed
    rm -f migrations/versions/"$REV_ID"_auto_migration.py 2>/dev/null || true
  elif [ $REVISION_EXIT_CODE -eq 0 ]; then
    echo "✨ New migration script ($REV_ID) generated automatically!"
  else
    echo "⚠️  Migration generation failed or was skipped."
    echo "$REVISION_OUTPUT"
  fi
fi

# 2. Apply all pending migrations (Always run this on startup)
echo "🆙 Applying pending migrations..."
alembic upgrade head
echo "✅ Database is now at the latest version!"

# 3. Start the application
echo "🚀 Launching CMatrix Backend..."
# If arguments are provided (like --reload), use them. Otherwise use defaults.
if [ $# -gt 0 ]; then
  exec uvicorn app.main:app "$@"
else
  exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-3012}
fi
