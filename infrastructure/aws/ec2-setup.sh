#!/bin/bash
# =============================================================================
# ec2-setup.sh — AWS EC2 Instance Bootstrap Script
#
# Purpose : Bootstraps a fresh Ubuntu EC2 instance with Docker
# Usage   : Run this as EC2 User Data, or SSH in and run manually
#           sudo bash infrastructure/aws/ec2-setup.sh
#
# What it installs:
#   - System updates
#   - Docker Engine + Docker Compose
#   - Basic firewall rules
# =============================================================================

set -euo pipefail

echo "============================================="
echo "  🚀 EC2 Bootstrap — DevOps Showcase Setup"
echo "============================================="

# ── 1. System Update ──────────────────────────────────────────────────────────
echo "[1/5] Updating system packages..."
apt-get update -y
apt-get upgrade -y

# ── 2. Install Docker ─────────────────────────────────────────────────────────
echo "[2/5] Installing Docker Engine..."
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# ── 3. Configure Docker ───────────────────────────────────────────────────────
echo "[3/5] Configuring Docker..."
systemctl start docker
systemctl enable docker

# Allow ec2-user / ubuntu to run Docker without sudo
usermod -aG docker ubuntu || true
usermod -aG docker ec2-user || true

# ── 4. Firewall Rules (UFW) ───────────────────────────────────────────────────
echo "[4/5] Setting up firewall rules..."
apt-get install -y ufw
ufw --force enable
ufw allow ssh           # Port 22
ufw allow 5000/tcp      # App port
ufw allow 80/tcp        # HTTP
ufw allow 443/tcp       # HTTPS

# ── 5. Verify Installation ────────────────────────────────────────────────────
echo "[5/5] Verifying installation..."
docker --version
docker compose version

echo ""
echo "============================================="
echo "  ✅ EC2 Bootstrap Complete!"
echo ""
echo "  Next steps:"
echo "  1. docker pull your-dockerhub-username/devops-showcase-app:latest"
echo "  2. bash scripts/deploy.sh production latest"
echo "  3. curl http://localhost:5000/health"
echo "============================================="
