# DevOps-CI-CD-End-to-End-Pipeline-Docker-AWS-Deployment.
This project simulates a real-world DevOps workflow — from writing code to deploying it automatically to the cloud. It covers the core skills expected of a DevOps Engineer: CI/CD pipelines, Docker, Kubernetes, cloud infrastructure, and monitoring.

Goal: Show that I can build, test, containerize, and deploy an application automatically — with zero manual steps after a git push.

🏗️ Architecture

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

🛠️ Tech Stack
LayerTechnologyPurposeApplicationPython / FlaskSimple REST APIContainerizationDockerPackage app + dependenciesOrchestrationKubernetesScale and manage containersCI/CDGitHub ActionsAutomate test → build → deployCloudAWS EC2Host the production serverRegistryDocker HubStore Docker imagesTestingPytestUnit testsMonitoringShell / Python scriptsHealth checks


📁 Project Structure

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

