# Multi-stage Docker build for AI Model Benchmarking System

# Stage 1: Python base
FROM python:3.11-slim as python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Node.js for examples
FROM node:20-slim as node-base

# Install Node.js dependencies if needed
WORKDIR /app
COPY examples/package.json* ./
RUN if [ -f package.json ]; then npm install; fi

# Stage 3: Final application
FROM python:3.11-slim

# Copy Python environment
COPY --from=python-base /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy Node.js if needed
COPY --from=node-base /usr/local/bin/node /usr/local/bin/node
COPY --from=node-base /usr/local/lib/node_modules /usr/local/lib/node_modules

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose ports
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command
CMD ["streamlit", "run", "dashboard/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]