#!/bin/bash

# CMatrix One-Line Installer
# Usage: curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/cmatrix/main/install.sh | bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔮 CMatrix Installer${NC}"
echo "--------------------------------"

# 1. Check Prerequisites
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker is not installed.${NC}"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# 2. Prepare Directory
INSTALL_DIR="cmatrix-app"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${BLUE}ℹ️  Directory $INSTALL_DIR already exists. Updating...${NC}"
else
    echo -e "${BLUE}xB6  Creating installation directory...${NC}"
    mkdir "$INSTALL_DIR"
fi
cd "$INSTALL_DIR"

# 3. Download Configuration
# NOTE: This URL points to your repository. Ensure the file exists on the 'api-key' branch.
COMPOSE_URL="https://raw.githubusercontent.com/Sajid576/cmatrix/api-key/docker-compose.release.yml"

echo -e "${BLUE}⬇️  Downloading configuration...${NC}"
# We use curl to fetch the file. We use -f to fail silently on server errors (like 404) so we can catch it.
if ! curl -fsSL "$COMPOSE_URL" -o docker-compose.yml; then
    echo -e "${RED}❌ Failed to download configuration.${NC}"
    echo "Error: The docker-compose.release.yml file was not found at:"
    echo "$COMPOSE_URL"
    echo "Please ensure you have pushed your latest changes (including docker-compose.release.yml) to GitHub."
    exit 1
fi

# 4. Configure Environment
if [ ! -f .env ]; then
    echo -e "${GREEN}⚙️  First-time setup detected.${NC}"
    echo "We need to configure a few settings."
    
    read -p "Enter your HuggingFace API Key (Press Enter to skip if not needed): " HF_KEY
    
    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "somerandomsecretkey12345")
    
    cat > .env <<EOF
HUGGINGFACE_API_KEY=$HF_KEY
SECRET_KEY=$SECRET_KEY
EOF
    echo -e "${GREEN}✅ Configuration saved to .env${NC}"
fi

# 5. Launch
echo -e "${BLUE}🚀 Pulling images and starting CMatrix...${NC}"
echo "This might take a few minutes depending on your internet speed."

# Stop and remove existing containers to avoid name conflicts
echo -e "${BLUE}🧹 Cleaning up old containers...${NC}"
docker rm -f cmatrix-postgres cmatrix-backend cmatrix-frontend 2>/dev/null || true

docker compose pull
docker compose up -d

echo "--------------------------------"
echo -e "${GREEN}✅ CMatrix is running!${NC}"
echo -e "👉 Access it here: ${BLUE}http://localhost:3000${NC}"
echo "To stop it, run: cd $INSTALL_DIR && docker compose down"
