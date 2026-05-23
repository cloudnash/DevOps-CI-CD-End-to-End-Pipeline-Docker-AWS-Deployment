# 🚀 Deployment Guide

How to deploy the app to AWS EC2 manually or via the CI/CD pipeline.

---

## 🌐 AWS EC2 Deployment (Manual)

### Step 1 — Launch an EC2 Instance

1. Go to **AWS Console → EC2 → Launch Instance**
2. Choose: **Ubuntu Server 22.04 LTS (Free Tier eligible)**
3. Instance type: `t2.micro` (Free Tier)
4. Create or select a **Key Pair** (download the `.pem` file)
5. Security Group — allow:
   - Port `22` (SSH)
   - Port `5000` (App)
   - Port `80` (HTTP, optional)

### Step 2 — Bootstrap the Server

```bash
# SSH into your instance
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Download and run the bootstrap script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/devops-cicd-showcase/main/infrastructure/aws/ec2-setup.sh
sudo bash ec2-setup.sh
```

### Step 3 — Deploy the Application

```bash
# Pull and run the Docker image
docker pull your-dockerhub-username/devops-showcase-app:latest
bash scripts/deploy.sh production latest
```

### Step 4 — Verify

```bash
curl http://YOUR_EC2_PUBLIC_IP:5000/health
# Expected: {"status": "healthy", ...}
```

---

## 🤖 Automated CI/CD Deployment

Once GitHub Secrets are configured (see `docs/SETUP.md`), every push to `main` will:

1. ✅ Lint the code
2. ✅ Run unit tests
3. ✅ Build and push Docker image to Docker Hub
4. ✅ SSH into EC2 and deploy the new image
5. ✅ Run a health check to confirm success

**No manual action needed.**

---

## ☸️ Kubernetes Deployment (Local with Minikube)

```bash
# Start Minikube
minikube start

# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl get services

# Access the app
minikube service devops-showcase-service
```

---

## 🔄 Rollback Strategy

If a deployment goes wrong:

```bash
# List available image tags
docker images your-dockerhub-username/devops-showcase-app

# Roll back to a previous version
bash scripts/deploy.sh production sha-abc1234
```
