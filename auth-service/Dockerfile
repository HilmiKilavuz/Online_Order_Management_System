# ============================================================================
# Auth Service Dockerfile
# ============================================================================
# This Dockerfile creates a production-ready container for the Auth Service
# ============================================================================

# Base image: Python 3.11 slim variant (smaller than full Python image)
FROM python:3.11-slim

# Metadata (good practice for documentation)
LABEL maintainer="auth-service-team"
LABEL description="Authentication microservice for Online Order Management System"
LABEL version="1.0.0"

# Environment variables
# PYTHONUNBUFFERED: Ensures Python output goes straight to logs (important for Docker)
# PYTHONDONTWRITEBYTECODE: Prevents .pyc files (saves space)
# PIP_NO_CACHE_DIR: Don't cache pip downloads (smaller image)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
# gcc: Required for compiling some Python packages
# postgresql-client: PostgreSQL tools (for RDS connection)
# Clean up apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
# If requirements don't change, Docker reuses this layer (faster builds)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
# Running as root is a security risk!
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port 5000 (documentation - doesn't actually publish the port)
EXPOSE 5000

# Health check - Docker will periodically check if container is healthy
# Calls /health endpoint every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command to run when container starts
CMD ["python", "app.py"]
