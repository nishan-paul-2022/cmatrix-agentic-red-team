#!/bin/bash

# CMatrix Docker Helper Script
# This script provides convenient commands for managing the CMatrix Docker containers

set -e

# Enable Docker BuildKit for optimized builds with caching
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to check if .env exists
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found!"
        print_info "Creating .env from .env.example..."
        cp .env.example .env
        print_warning "Please edit .env and add your SECRET_KEY"
        exit 1
    fi
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Determine docker compose command
get_compose_cmd() {
    if docker compose version > /dev/null 2>&1; then
        echo "docker compose"
    elif command -v docker-compose > /dev/null 2>&1; then
        echo "docker-compose"
    else
        print_error "Neither 'docker compose' nor 'docker-compose' found. Please install Docker Compose."
        exit 1
    fi
}

COMPOSE_CMD=$(get_compose_cmd)


# Show usage
show_usage() {
    cat << EOF
${GREEN}CMatrix Docker Helper${NC} ${BLUE}(Optimized with BuildKit)${NC}

Usage: ./docker.sh [command] [options]

${YELLOW}Commands:${NC}
  ${BLUE}start${NC}          Start all services in production mode
  ${BLUE}dev${NC}            Start all services in development mode (with hot reload)
  ${BLUE}stop${NC}           Stop all services
  ${BLUE}restart${NC}        Restart all services
  ${BLUE}logs${NC}           Show logs from all services
  ${BLUE}logs-app-backend${NC}   Show app-app-backend logs only
  ${BLUE}logs-app-frontend${NC}  Show app-app-frontend logs only
  ${BLUE}logs-db${NC}        Show database logs only
  ${BLUE}build${NC}          Build all Docker images (with optimized caching)
  ${BLUE}build --verbose${NC} Build with detailed progress output
  ${BLUE}rebuild${NC}        Rebuild all images from scratch (no cache, slower)
  ${BLUE}clean${NC}          Stop and remove all containers, networks, and volumes
  ${BLUE}status${NC}         Show status of all services
  ${BLUE}shell-app-backend${NC}  Open a shell in the app-app-backend container
  ${BLUE}shell-app-frontend${NC} Open a shell in the app-app-frontend container
  ${BLUE}shell-db${NC}       Open a shell in the database container
  ${BLUE}health${NC}         Check health status of all services
  ${BLUE}setup${NC}          Initial setup (create .env file)

${YELLOW}Examples:${NC}
  ./docker.sh start           # Start in production mode
  ./docker.sh dev             # Start in development mode
  ./docker.sh build           # Build with optimizations (fast)
  ./docker.sh build --verbose # Build with detailed output
  ./docker.sh logs            # View all logs
  ./docker.sh clean           # Clean up everything

${YELLOW}Build Optimization:${NC}
  • Heavy ML dependencies cached separately for faster rebuilds
  • BuildKit cache mounts enabled for pip downloads
  • Typical rebuild time: 30 seconds (vs 10-15 minutes before)

EOF
}

# Setup environment
setup() {
    print_info "Setting up CMatrix Docker environment..."

    if [ -f .env ]; then
        print_warning ".env file already exists"
        read -p "Do you want to overwrite it? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Keeping existing .env file"
            return
        fi
    fi

    cp .env.example .env
    print_success "Created .env file"
    print_warning "Please edit .env and add your SECRET_KEY"
    print_info "You can edit it with: nano .env"
}

# Start services in production mode
start_prod() {
    check_docker
    check_env
    print_info "Starting CMatrix in production mode..."
    $COMPOSE_CMD up -d --remove-orphans
    print_success "Services started!"
    print_info "Frontend: http://localhost:3000"
    print_info "Backend: http://localhost:8000"
    print_info "Database: Port 5432 (Internal)"
    print_info "API Docs: http://localhost:8000/docs"
}

# Start services in development mode
start_dev() {
    check_docker
    check_env
    print_info "Starting CMatrix in development mode..."
    $COMPOSE_CMD -f docker-compose.yml -f docker-compose.dev.yml up
}

# Stop services
stop() {
    check_docker
    print_info "Stopping all services..."
    $COMPOSE_CMD down
    print_success "Services stopped"
}

# Restart services
restart() {
    check_docker
    print_info "Restarting all services..."
    $COMPOSE_CMD restart
    print_success "Services restarted"
}

# Show logs
show_logs() {
    check_docker
    $COMPOSE_CMD logs -f
}

# Show app-app-backend logs
show_backend_logs() {
    check_docker
    $COMPOSE_CMD logs -f backend
}

# Show app-app-frontend logs
show_frontend_logs() {
    check_docker
    $COMPOSE_CMD logs -f frontend
}

# Show database logs
show_db_logs() {
    check_docker
    $COMPOSE_CMD logs -f postgres
}

# Build images
build() {
    check_docker
    print_info "Building Docker images with optimizations..."
    print_info "Using BuildKit cache mounts for faster builds"

    # Check if user wants detailed progress
    if [[ "${2}" == "--verbose" ]] || [[ "${2}" == "-v" ]]; then
        print_info "Building with detailed progress..."
        BUILDKIT_PROGRESS=plain $COMPOSE_CMD build
    else
        $COMPOSE_CMD build
    fi

    print_success "Build complete"
    print_info "Tip: Heavy ML dependencies are cached separately for faster rebuilds"
    print_info "     Use './docker.sh build --verbose' for detailed build output"
}

# Rebuild images from scratch
rebuild() {
    check_docker
    print_warning "Rebuilding from scratch will clear ALL caches (including heavy ML dependencies)"
    print_info "This will take 10-15 minutes to re-download all packages"
    print_info "Consider using './docker.sh build' instead for faster incremental builds"
    echo ""
    read -p "Are you sure you want to rebuild from scratch? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Rebuilding Docker images from scratch..."
        $COMPOSE_CMD build --no-cache
        print_success "Rebuild complete"
    else
        print_info "Rebuild cancelled. Using './docker.sh build' instead..."
        build
    fi
}

# Clean up everything
clean() {
    check_docker
    print_warning "This will remove all containers, networks, and volumes"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cleaning up..."
        $COMPOSE_CMD down -v
        print_success "Cleanup complete"
    else
        print_info "Cleanup cancelled"
    fi
}

# Show status
status() {
    check_docker
    print_info "Service Status:"
    $COMPOSE_CMD ps
}

# Open shell in backend
shell_backend() {
    check_docker
    print_info "Opening shell in app-app-backend container..."
    $COMPOSE_CMD exec app-backend bash
}

# Open shell in frontend
shell_frontend() {
    check_docker
    print_info "Opening shell in app-app-frontend container..."
    $COMPOSE_CMD exec app-frontend sh
}

# Open shell in database
shell_db() {
    check_docker
    print_info "Opening shell in database container..."
    $COMPOSE_CMD exec postgres bash
}

# Check health
check_health() {
    check_docker
    print_info "Checking service health..."

    echo ""
    print_info "Database Health:"
    if docker inspect cmatrix-postgres --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "Database is running"
    else
        print_error "Database is not running or unhealthy"
    fi

    echo ""
    print_info "App-Backend Health:"
    if docker inspect cmatrix-app-backend --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "App-Backend (Production) is running"
    elif docker inspect cmatrix-app-backend-dev --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "App-Backend (Development) is running"
    else
        print_error "Backend is not running or unhealthy"
    fi

    echo ""
    print_info "App-Frontend Health:"
    if docker inspect cmatrix-app-frontend --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "App-Frontend (Production) is running"
    elif docker inspect cmatrix-app-frontend-dev --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "App-Frontend (Development) is running"
    else
        print_error "Frontend is not running or unhealthy"
    fi
}

# Main script logic
case "${1:-}" in
    start)
        start_prod
        ;;
    dev)
        start_dev
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        show_logs
        ;;
    logs-app-backend)
        show_backend_logs
        ;;
    logs-app-frontend)
        show_frontend_logs
        ;;
    logs-db)
        show_db_logs
        ;;
    build)
        build
        ;;
    rebuild)
        rebuild
        ;;
    clean)
        clean
        ;;
    status)
        status
        ;;
    shell-app-backend)
        shell_backend
        ;;
    shell-app-frontend)
        shell_frontend
        ;;
    shell-db)
        shell_db
        ;;
    health)
        check_health
        ;;
    setup)
        setup
        ;;
    *)
        show_usage
        ;;
esac
