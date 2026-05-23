#!/bin/bash
# =============================================================================
# deploy.sh — Manual Deployment Script
# Usage: bash scripts/deploy.sh [environment] [version]
#
# Examples:
#   bash scripts/deploy.sh production 1.2.0
#   bash scripts/deploy.sh staging latest
# =============================================================================

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
ENVIRONMENT="${1:-staging}"
VERSION="${2:-latest}"
DOCKER_IMAGE="your-dockerhub-username/devops-showcase-app"
CONTAINER_NAME="devops-showcase-app"
PORT=5000

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "=================================================="
echo "  🚀 DevOps Showcase — Deployment Script"
echo "  Environment : $ENVIRONMENT"
echo "  Version     : $VERSION"
echo "  Image       : $DOCKER_IMAGE:$VERSION"
echo "=================================================="
echo -e "${NC}"

# ── Step 1: Pull latest image ─────────────────────────────────────────────────
echo -e "${YELLOW}[1/4] Pulling Docker image...${NC}"
docker pull "$DOCKER_IMAGE:$VERSION"

# ── Step 2: Stop existing container ──────────────────────────────────────────
echo -e "${YELLOW}[2/4] Stopping existing container (if any)...${NC}"
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# ── Step 3: Run new container ─────────────────────────────────────────────────
echo -e "${YELLOW}[3/4] Starting new container...${NC}"
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p "$PORT:$PORT" \
  -e ENVIRONMENT="$ENVIRONMENT" \
  -e APP_VERSION="$VERSION" \
  "$DOCKER_IMAGE:$VERSION"

# ── Step 4: Health check ──────────────────────────────────────────────────────
echo -e "${YELLOW}[4/4] Running health check...${NC}"
sleep 5

if curl -sf "http://localhost:$PORT/health" > /dev/null; then
  echo -e "${GREEN}"
  echo "=================================================="
  echo "  ✅ Deployment successful!"
  echo "  App is running at: http://localhost:$PORT"
  echo "=================================================="
  echo -e "${NC}"
else
  echo "❌ Health check failed! Rolling back..."
  docker stop "$CONTAINER_NAME" || true
  exit 1
fi
