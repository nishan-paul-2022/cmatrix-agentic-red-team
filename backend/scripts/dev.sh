#!/bin/bash

# Development server startup script
echo "🚀 Starting CMatrix Backend (Development Mode)"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration!"
    exit 1
fi

# Run the application
echo "🎯 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app
