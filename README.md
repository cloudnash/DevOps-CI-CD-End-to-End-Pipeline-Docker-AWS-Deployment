# DevOps-CI-CD-End-to-End-Pipeline-Docker-AWS-Deployment.
This project simulates a real-world DevOps workflow — from writing code to deploying it automatically to the cloud. It covers the core skills expected of a DevOps Engineer: CI/CD pipelines, Docker, Kubernetes, cloud infrastructure, and monitoring.

Goal: Show that I can build, test, containerize, and deploy an application automatically — with zero manual steps after a git push.

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
|---|---|
| **Application** | Python / Flask | Simple REST API |
| **Containerization** | Docker | Package app + dependencies |
| **Orchestration** | Kubernetes | Scale and manage containers |
| **CI/CD** GitHub** | Actions | Automate test → build → deploy |
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

---


Key features of the pipeline:

🔴 Fails fast — if tests fail, nothing gets deployed
🐳 Docker layer caching — faster builds on repeated runs
🔐 Secrets management — credentials stored in GitHub Secrets, never in code
🩺 Post-deploy health check — confirms the app is alive after deployment
🔄 Zero-downtime deploy — old container stays up until new one is healthy

## 🚀 Quick Start

