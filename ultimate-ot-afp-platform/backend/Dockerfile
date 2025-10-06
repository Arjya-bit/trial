# Ultimate OT-AFP Platform - Backend Dockerfile

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libmagic1 \
    libmagic-dev \
    libewf-dev \
    libewf2 \
    sleuthkit \
    volatility-tools \
    yara \
    libyara-dev \
    tshark \
    tcpdump \
    netcat-openbsd \
    curl \
    wget \
    git \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN groupadd -r otapp && useradd -r -g otapp otapp

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/models /app/uploads && \
    chown -R otapp:otapp /app

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app\n\
if [ "$ENVIRONMENT" = "development" ]; then\n\
    python main.py\n\
else\n\
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4\n\
fi' > /app/start.sh && chmod +x /app/start.sh

# Switch to non-root user
USER otapp

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["/app/start.sh"]