# Multi-stage Dockerfile for CMatrix Backend (Optimized for caching)

# Stage 1: Base image with system dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies and common security/monitoring tools
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    nmap \
    curl \
    procps \
    iproute2 \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 appuser

# Stage 2: Install base (heavy) dependencies
FROM base as base-deps

WORKDIR /app

# Install heavy ML/AI dependencies first (cached unless requirements.base.txt changes)
COPY requirements.base.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.base.txt

# Stage 3: Install project dependencies
FROM base-deps as dependencies

# Install lighter project dependencies (cached unless requirements.project.txt changes)
COPY requirements.project.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.project.txt

# Stage 4: Production
FROM base as production

WORKDIR /app

# Copy all installed dependencies from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY data/ ./data/
COPY scripts/ ./scripts/
COPY warmup_models.py .
COPY .env.example .env.example

# Create necessary directories and warmup models
RUN chown -R appuser:appuser /app

# Pre-load ML models to cache them (run as root before switching to appuser)
# This ensures fast startup and no slow first requests
# Use cache mount to persist models between builds
RUN --mount=type=cache,target=/root/.cache/huggingface \
    python warmup_models.py || echo "⚠️  Model warmup failed, models will load on first request"

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
