#!/bin/bash

# Quick setup script for the new backend structure

echo "🚀 CMatrix Backend - Quick Setup"
echo "================================="
echo ""

# 1. System Tools Check
echo "🔍 Checking system requirements..."
if ! command -v nmap &> /dev/null; then
    echo "❌ Error: nmap is not installed."
    echo "   Please install it: sudo apt install nmap"
    exit 1
else
    echo "✅ nmap found"
fi

# 2. Python Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing dependencies..."
pip install -r requirements.txt

# 3. Configuration
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please edit .env and add your HUGGINGFACE_API_KEY"
else
    echo "✅ .env file exists"
fi

# 4. Directory Structure
echo "📁 Creating necessary directories..."
mkdir -p logs/audit_logs
mkdir -p data

# 5. Data Initialization


if [ ! -f "data/auth_config.json" ]; then
    echo "📝 Creating default data/auth_config.json..."
    echo '{}' > data/auth_config.json
fi

# 6. Permissions
echo "🔐 Setting script permissions..."
chmod +x scripts/*.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your HUGGINGFACE_API_KEY"
echo "2. Run: ./scripts/dev.sh"
echo "3. Visit: http://localhost:8000/docs"
echo ""
