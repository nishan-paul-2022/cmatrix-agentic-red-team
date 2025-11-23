#!/bin/bash

# CMatrix Docker Helper Script
# This script provides convenient commands for managing the CMatrix Docker containers

set -e

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
        print_warning "Please edit .env and add your HUGGINGFACE_API_KEY and SECRET_KEY"
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
${GREEN}CMatrix Docker Helper${NC}

Usage: ./docker.sh [command]

${YELLOW}Commands:${NC}
  ${BLUE}start${NC}          Start all services in production mode
  ${BLUE}dev${NC}            Start all services in development mode (with hot reload)
  ${BLUE}stop${NC}           Stop all services
  ${BLUE}restart${NC}        Restart all services
  ${BLUE}logs${NC}           Show logs from all services
  ${BLUE}logs-backend${NC}   Show backend logs only
  ${BLUE}logs-frontend${NC}  Show frontend logs only
  ${BLUE}logs-db${NC}        Show database logs only
  ${BLUE}build${NC}          Build all Docker images
  ${BLUE}rebuild${NC}        Rebuild all images from scratch (no cache)
  ${BLUE}clean${NC}          Stop and remove all containers, networks, and volumes
  ${BLUE}status${NC}         Show status of all services
  ${BLUE}shell-backend${NC}  Open a shell in the backend container
  ${BLUE}shell-frontend${NC} Open a shell in the frontend container
  ${BLUE}shell-db${NC}       Open a shell in the database container
  ${BLUE}health${NC}         Check health status of all services
  ${BLUE}setup${NC}          Initial setup (create .env file)

${YELLOW}Examples:${NC}
  ./docker.sh start       # Start in production mode
  ./docker.sh dev         # Start in development mode
  ./docker.sh logs        # View all logs
  ./docker.sh clean       # Clean up everything

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
    print_warning "Please edit .env and add your HUGGINGFACE_API_KEY and SECRET_KEY"
    print_info "You can edit it with: nano .env"
}

# Start services in production mode
start_prod() {
    check_docker
    check_env
    print_info "Starting CMatrix in production mode..."
    $COMPOSE_CMD up -d
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

# Show backend logs
show_backend_logs() {
    check_docker
    $COMPOSE_CMD logs -f backend
}

# Show frontend logs
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
    print_info "Building Docker images..."
    $COMPOSE_CMD build
    print_success "Build complete"
}

# Rebuild images from scratch
rebuild() {
    check_docker
    print_info "Rebuilding Docker images from scratch..."
    $COMPOSE_CMD build --no-cache
    print_success "Rebuild complete"
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
    print_info "Opening shell in backend container..."
    $COMPOSE_CMD exec backend bash
}

# Open shell in frontend
shell_frontend() {
    check_docker
    print_info "Opening shell in frontend container..."
    $COMPOSE_CMD exec frontend sh
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
    print_info "Backend Health:"
    if docker inspect cmatrix-backend --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "Backend is running"
    else
        print_error "Backend is not running or unhealthy"
    fi
    
    echo ""
    print_info "Frontend Health:"
    if docker inspect cmatrix-frontend --format='{{.State.Health.Status}}' 2>/dev/null; then
        print_success "Frontend is running"
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
    logs-backend)
        show_backend_logs
        ;;
    logs-frontend)
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
    shell-backend)
        shell_backend
        ;;
    shell-frontend)
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
