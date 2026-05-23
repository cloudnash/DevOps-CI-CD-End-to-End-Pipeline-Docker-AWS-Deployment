# ─────────────────────────────────────────────────────────────────────────────
# Stage 1: Builder — install dependencies in an isolated layer
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /install

COPY app/requirements.txt .

# Install dependencies into a local folder (keeps final image lean)
RUN pip install --prefix=/install/deps --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────────────────────────────────────────
# Stage 2: Production Image — copy only what's needed
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="your-email@example.com"
LABEL version="1.0.0"
LABEL description="DevOps Showcase App - Flask API"

# Create a non-root user for security best practice
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /home/appuser/app

# Copy installed packages from builder stage
COPY --from=builder /install/deps /usr/local

# Copy application source
COPY app/ .

# Set ownership
RUN chown -R appuser:appuser /home/appuser/app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 5000

# Environment defaults (can be overridden at runtime)
ENV ENVIRONMENT=production \
    APP_VERSION=1.0.0 \
    PORT=5000

# Health check so Docker/Kubernetes knows if the app is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Start with Gunicorn (production-grade WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
