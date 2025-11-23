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
    echo -e "${BLUE}📁  Creating installation directory...${NC}"
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

# 4. Download Sample LLM Configuration
CONFIG_SAMPLE_URL="https://raw.githubusercontent.com/Sajid576/cmatrix/api-key/llm_config_sample.json"

echo -e "${BLUE}⬇️  Downloading sample LLM configuration...${NC}"
if curl -fsSL "$CONFIG_SAMPLE_URL" -o llm_config_sample.json 2>/dev/null; then
    echo -e "${GREEN}✅ Sample configuration downloaded${NC}"
else
    echo -e "${BLUE}ℹ️  Could not download sample config (optional)${NC}"
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
echo ""
echo -e "👉 Access it here: ${BLUE}http://localhost:3000${NC}"
echo ""
echo -e "${GREEN}📝 Next Steps:${NC}"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Create your admin account (first-time setup)"
echo "3. Navigate to Settings → LLM Configuration"
echo "4. Import the sample config file: llm_config_sample.json"
echo "5. Edit the profiles to add your API keys"
echo "6. Activate a profile to start using CMatrix"
echo ""
echo -e "${BLUE}ℹ️  Sample config location:${NC} $PWD/llm_config_sample.json"
echo ""
echo "To stop CMatrix, run: cd $INSTALL_DIR && docker compose down"

