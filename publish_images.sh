#!/bin/bash

# Exit on error
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for docker
if ! command_exists docker; then
    echo "Error: docker is not installed."
    exit 1
fi

# Get Docker Hub Username
if [ -z "$1" ]; then
    read -p "Enter your Docker Hub username: " USERNAME
else
    USERNAME=$1
fi

if [ -z "$USERNAME" ]; then
    echo "Error: Username cannot be empty."
    exit 1
fi

if [[ "$USERNAME" == *"@"* ]]; then
    echo "Error: It looks like you entered an email address."
    echo "Please enter your Docker Hub USERNAME (e.g., 'nishanpaul'), not your email."
    exit 1
fi

VERSION="latest"
read -p "Enter version tag (default: latest): " INPUT_VERSION
if [ ! -z "$INPUT_VERSION" ]; then
    VERSION=$INPUT_VERSION
fi

echo "----------------------------------------------------------------"
echo "Preparing to build and push images for user: $USERNAME"
echo "Version: $VERSION"
echo "----------------------------------------------------------------"

# Login check
echo "Checking Docker login status..."
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker daemon is not running."
    exit 1
fi

# We can't easily check if logged in to Hub specifically without trying to push, 
# but we can remind the user.
echo "Please ensure you are logged in to Docker Hub."
echo "Run 'docker login' if you haven't already."
read -p "Press Enter to continue..."

# Build and Push Backend
echo "----------------------------------------------------------------"
echo "Building Backend Image..."
echo "----------------------------------------------------------------"
docker build -t $USERNAME/cmatrix-backend:$VERSION ./backend
echo "Pushing Backend Image..."
if ! docker push $USERNAME/cmatrix-backend:$VERSION; then
    echo "----------------------------------------------------------------"
    echo "❌ Error: Failed to push the backend image."
    echo "This is usually because you are not logged in or the username is incorrect."
    echo "Please run 'docker login' and try again."
    echo "----------------------------------------------------------------"
    exit 1
fi

# Build and Push Frontend
echo "----------------------------------------------------------------"
echo "Building Frontend Image..."
echo "----------------------------------------------------------------"
docker build -t $USERNAME/cmatrix-frontend:$VERSION ./frontend
echo "Pushing Frontend Image..."
if ! docker push $USERNAME/cmatrix-frontend:$VERSION; then
    echo "----------------------------------------------------------------"
    echo "❌ Error: Failed to push the frontend image."
    echo "Please run 'docker login' and try again."
    echo "----------------------------------------------------------------"
    exit 1
fi

echo "----------------------------------------------------------------"
echo "Images pushed successfully!"
echo "----------------------------------------------------------------"

# Generate docker-compose.release.yml
echo "Generating docker-compose.release.yml..."

cat > docker-compose.release.yml <<EOF
services:
  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    container_name: cmatrix-postgres
    environment:
      - POSTGRES_USER=cmatrix
      - POSTGRES_PASSWORD=cmatrix
      - POSTGRES_DB=cmatrix
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - cmatrix-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cmatrix"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"

  # Backend Service
  backend:
    image: $USERNAME/cmatrix-backend:$VERSION
    container_name: cmatrix-backend
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - DATABASE_URL=postgresql+asyncpg://cmatrix:cmatrix@postgres:5432/cmatrix
      # You should change this secret key in production!
      - SECRET_KEY=change-this-in-production-make-it-very-long-and-random
      # Add your HuggingFace API key here if needed, or use a .env file
      - HUGGINGFACE_API_KEY=\${HUGGINGFACE_API_KEY}
      - HUGGINGFACE_MODEL=\${HUGGINGFACE_MODEL:-DeepHat/DeepHat-V1-7B}
    volumes:
      - ./cmatrix_data/logs:/app/logs
      - ./cmatrix_data/data:/app/data
    networks:
      - cmatrix-network
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  # Frontend Service
  frontend:
    image: $USERNAME/cmatrix-frontend:$VERSION
    container_name: cmatrix-frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PYTHON_BACKEND_URL=http://backend:8000
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - cmatrix-network
    restart: unless-stopped

networks:
  cmatrix-network:
    driver: bridge

volumes:
  postgres_data:
    driver: local
EOF

echo "docker-compose.release.yml has been created."
echo "You can share this file with others. They can run 'docker-compose -f docker-compose.release.yml up -d' to start the application."
