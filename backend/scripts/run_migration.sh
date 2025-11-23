#!/bin/bash
# Script to run database migrations

echo "Running LLM models migration..."

# Check if running in Docker or local
if [ -f "/.dockerenv" ]; then
    # Running in Docker
    psql -U $POSTGRES_USER -d $POSTGRES_DB -f /app/migrations/002_add_llm_models.sql
else
    # Running locally with Docker Compose
    docker-compose exec -T postgres psql -U cmatrix -d cmatrix < migrations/002_add_llm_models.sql
fi

echo "Migration completed successfully!"
