#!/bin/bash

# Docker Build Optimization Setup Script
# This script enables BuildKit and provides helpful build commands

set -e

echo "🚀 CMatrix Docker Build Optimization Setup"
echo "=========================================="
echo ""

# Enable BuildKit
echo "✓ Enabling Docker BuildKit..."
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Add to shell profile if not already there
SHELL_RC="${HOME}/.bashrc"
if [ -f "${HOME}/.zshrc" ]; then
    SHELL_RC="${HOME}/.zshrc"
fi

if ! grep -q "DOCKER_BUILDKIT=1" "$SHELL_RC" 2>/dev/null; then
    echo ""
    echo "Adding BuildKit environment variables to $SHELL_RC..."
    echo "" >> "$SHELL_RC"
    echo "# Enable Docker BuildKit for better caching" >> "$SHELL_RC"
    echo "export DOCKER_BUILDKIT=1" >> "$SHELL_RC"
    echo "export COMPOSE_DOCKER_CLI_BUILD=1" >> "$SHELL_RC"
    echo "✓ BuildKit enabled permanently in $SHELL_RC"
else
    echo "✓ BuildKit already enabled in $SHELL_RC"
fi

echo ""
echo "📦 Optimization Details:"
echo "  - Split requirements: Heavy ML deps cached separately"
echo "  - BuildKit cache mounts: Pip downloads cached across builds"
echo "  - Multi-stage builds: Minimal production image size"
echo ""

echo "🔧 Available Commands:"
echo ""
echo "  # Clean build (first time or after major changes):"
echo "  docker-compose build --no-cache"
echo ""
echo "  # Normal build (uses cache):"
echo "  docker-compose build"
echo ""
echo "  # Rebuild only backend:"
echo "  docker-compose build backend worker"
echo ""
echo "  # View build progress:"
echo "  BUILDKIT_PROGRESS=plain docker-compose build backend"
echo ""
echo "  # Clean old images and cache:"
echo "  docker system prune -a"
echo ""

echo "📊 Expected Build Times:"
echo "  - First build: ~10-15 minutes (downloads all dependencies)"
echo "  - Rebuild (no changes): ~5 seconds (fully cached)"
echo "  - Rebuild (code changes): ~10 seconds (only copies new code)"
echo "  - Rebuild (project deps change): ~30 seconds (reuses ML packages)"
echo "  - Rebuild (base deps change): ~3 minutes (reuses downloads)"
echo ""

echo "✅ Setup complete!"
echo ""
echo "To start building with optimizations, run:"
echo "  docker-compose build"
echo ""
