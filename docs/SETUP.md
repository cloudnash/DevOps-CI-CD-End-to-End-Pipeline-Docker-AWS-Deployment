# 🛠️ Setup Guide

This guide walks you through running the project locally and setting up the full CI/CD pipeline.

---

## Prerequisites

| Tool | Minimum Version | Check |
|------|----------------|-------|
| Python | 3.11+ | `python --version` |
| Docker | 24.0+ | `docker --version` |
| Git | 2.40+ | `git --version` |

---

## 🖥️ Option A — Run Locally (Python)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/devops-cicd-showcase.git
cd devops-cicd-showcase

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r app/requirements.txt

# 4. Run the app
cd app
python app.py
```

Visit: http://localhost:5000

---

## 🐳 Option B — Run with Docker

```bash
# Build the image
docker build -f docker/Dockerfile -t devops-showcase-app .

# Run the container
docker run -d -p 5000:5000 --name devops-app devops-showcase-app

# Check it's running
curl http://localhost:5000/health
```

---

## 🐙 Option C — Run with Docker Compose (Recommended)

```bash
cd docker
docker-compose up --build
```

---

## 🧪 Running Tests

```bash
# Make sure dependencies are installed
pip install -r app/requirements.txt

# Run all tests
pytest app/tests/ -v

# Run with coverage
pytest app/tests/ -v --cov=app
```

---

## 🔑 Setting Up GitHub Secrets (for CI/CD)

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**

| Secret Name | Description |
|-------------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (not password) |
| `SERVER_HOST` | IP address of your AWS EC2 instance |
| `SERVER_USER` | SSH username (`ubuntu` for Ubuntu AMI) |
| `SERVER_SSH_KEY` | Private SSH key for EC2 access |

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Home — returns app info |
| `GET /health` | Health check — used by K8s probes |
| `GET /info` | System info — useful for debugging |
