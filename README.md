# DevOps-CI-CD-End-to-End-Pipeline-Docker-AWS-Deployment.
This project simulates a real-world DevOps workflow — from writing code to deploying it automatically to the cloud. It covers the core skills expected of a DevOps Engineer: CI/CD pipelines, Docker, Kubernetes, cloud infrastructure, and monitoring.

## 📌 Project Overview

This project simulates a real-world DevOps workflow — from writing code to deploying it automatically to the cloud. It covers the core skills expected of a DevOps Engineer: CI/CD pipelines, Docker, Kubernetes, cloud infrastructure, and monitoring.

> **Goal:** Show that I can build, test, containerize, and deploy an application automatically — with zero manual steps after a git push.

---

## 🏗️Architecture

```
Developer Pushes Code
        │
        ▼
┌──────────────────────────────────────────────────┐
│              GitHub Actions CI/CD                │
│                                                  │
│  [Lint] → [Test] → [Docker Build] → [Deploy]    │
└────────────────────────┬─────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    Docker Hub      AWS EC2        Kubernetes
    (Image Store)  (VM Deploy)   (Orchestration)
          │              │
          └──────────────┘
                 │
                 ▼
         Flask Application
         ├── GET /          → App Info
         ├── GET /health    → Health Check
         └── GET /info      → System Info
```

---

## 🛠️Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Application** | Python / Flask | Simple REST API |
| **Containerization** | Docker | Package app + dependencies |
| **Orchestration** | Kubernetes | Scale and manage containers |
| **CI/CD** | GitHub Actions | Automate test → build → deploy |
| **Cloud** | AWSEC2 | Host the production server |
| **Registry** | Docker Hub | Store Docker images |
| **Testing** | Pytest | Unit tests |
| **Monitoring** | Shell / Python scripts | Health checks |

---

## 📁 Project Structure

```
devops-cicd-showcase/
│
├── 📂 app/                          # Flask application
│   ├── app.py                       # Main application + API routes
│   ├── requirements.txt             # Python dependencies
│   └── tests/
│       └── test_app.py              # Unit tests (Pytest)
│
├── 📂 docker/                       # Containerization
│   ├── Dockerfile                   # Multi-stage Docker build
│   └── docker-compose.yml           # Local development stack
│
├── 📂 .github/workflows/            # CI/CD Automation
│   └── ci-cd.yml                    # GitHub Actions pipeline
│
├── 📂 k8s/                          # Kubernetes manifests
│   ├── deployment.yaml              # Pod deployment + rolling updates
│   └── service.yaml                 # LoadBalancer + Autoscaler (HPA)
│
├── 📂 scripts/                      # Automation scripts
│   ├── monitor.sh                   # Live health monitoring loop
│   ├── deploy.sh                    # Manual deployment helper
│   └── health_check.py             # Python health checker
│
├── 📂 infrastructure/
│   └── aws/
│       └── ec2-setup.sh             # EC2 bootstrap script
│
├── 📂 docs/
│   ├── SETUP.md                     # Local setup guide
│   └── DEPLOYMENT.md                # Cloud deployment guide
│
└── README.md                        # You are here

```

---

## ⚙️CI/CD Pipeline

The pipeline runs automatically on every git push to main or develop.

```

Push to GitHub
      │
      ▼
 ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
 │  🔍 Lint    │────▶│  🧪 Test   │────▶│  🐳 Docker      │────▶│  🚀 Deploy  │
 │  (Flake8)   │     │  (Pytest)   │     │  Build & Push   │     │  (SSH→EC2)  │
 └─────────────┘     └─────────────┘     └─────────────────┘     └──────────────┘
                           │                                             │
                     Fails? → ❌                                   Health Check
                     No Deploy                                       Pass? → ✅

```



### Key features of the pipeline:

- Fails fast — if tests fail, nothing gets deployed
- Docker layer caching — faster builds on repeated runs
- Secrets management — credentials stored in GitHub Secrets, never in code
- Post-deploy health check — confirms the app is alive after deployment
- Zero-downtime deploy — old container stays up until new one is healthy

---

## 🚀 Quick Start

### Run Locally

```
git clone https://github.com/YOUR_USERNAME/devops-cicd-showcase.git
cd devops-cicd-showcase

pip install -r app/requirements.txt
cd app && python app.py
```
### Run with Docker

```
docker build -f docker/Dockerfile -t devops-showcase-app .
docker run -p 5000:5000 devops-showcase-app
```

### Run with Docker Compose
```
cd docker && docker-compose up --build
```

### Run Tests
```
pytest app/tests/ -v
```

### Test the API:
```
curl http://localhost:5000/          # App info
curl http://localhost:5000/health    # Health check
curl http://localhost:5000/info      # System info
```
---

## ☁️ AWS Deployment

```
# 1. Launch Ubuntu EC2 instance (t2.micro — Free Tier)
# 2. SSH in and run the bootstrap script
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
sudo bash infrastructure/aws/ec2-setup.sh

# 3. Deploy the app
bash scripts/deploy.sh production latest

# 4. Verify
curl http://YOUR_EC2_IP:5000/health
```

### Full walkthrough: docs/DEPLOYMENT.md

---

## 📊 Monitoring
```
# Continuous health monitoring (checks every 30s)
bash scripts/monitor.sh http://localhost:5000 30

# One-time health check with verbose output
python scripts/health_check.py --url http://localhost:5000 --verbose
```

Sample output:

```
=======================================================
  🔍 Health Check Report — 2024-11-01 10:30:00 UTC
  Base URL: http://localhost:5000
=======================================================

  ✅ /health       → HEALTHY       [HTTP 200] 12ms
  ✅ /             → HEALTHY       [HTTP 200] 8ms
  ✅ /info         → HEALTHY       [HTTP 200] 9ms

=======================================================
  ✅ All checks passed. Application is healthy.
=======================================================
```

---

## ☸️ Kubernetes (Local with Minikube)

```
minikube start
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get pods          # Watch pods start
kubectl get services      # Get external IP
```

Features configured:

- Rolling updates — zero-downtime deployments
- Liveness & Readiness probes — automatic restart on crash
- Horizontal Pod Autoscaler — scales 2–5 pods based on CPU load
- Resource limits — prevents runaway memory/CPU usage

---

## 🔑 GitHub Secrets Required

### To enable the full CI/CD pipeline, add these in Settings → Secrets → Actions:

| Secret | Description |
|---|---|
| **DOCKERHUB_USERNAME** | Docker Hub username |
| **DOCKERHUB_TOKEN** | Docker Hub access token |
| **SERVER_HOSTEC2** | public IP address |
| **SERVER_USER** | SSH user (ubuntu) |
| **SERVER_SSH_KEY** | EC2 private key (.pem content) |

---

## 📚 What I Learned

| Skill | Implemented In |
|---|---|
| **CI/CD pipelines** | .github/workflows/ci-cd.yml |
| **Docker multi-stage** | buildsdocker/Dockerfile |
| **Container orchestration** | k8s/deployment.yaml |
| **Linux scriptings** | cripts/monitor.sh, deploy.sh |
| **AWS EC2 setup** | infrastructure/aws/ec2-setup.sh |
| **Python scripting** | scripts/health_check.py |
| **Unit testing** | app/tests/test_app.py |
| **Git branching** | main / develop branch strategy |

---

## 🤝 Contributing

This is an internship learning project. Feel free to fork, explore, and learn from it!

---

*📞 Contact*
---

- GitHub: [@cloudnash](https://github.com/cloudnash)
- LinkedIn: [Nashit Ahmad](https://in.linkedin.com/in/nashitahmad)
- Email: nashitakerfeldt@gmail.com

---
