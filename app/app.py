"""
DevOps Showcase App - Simple Flask Application
Author: Your Name
Purpose: Demonstrates CI/CD pipeline, Docker containerization, and cloud deployment
"""

from flask import Flask, jsonify
import os
import datetime
import platform

app = Flask(__name__)

# ── Config ──────────────────────────────────────────────────────────────────
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return jsonify({
        "message": "🚀 DevOps Showcase App is running!",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/health")
def health():
    """Health check endpoint used by load balancers and Kubernetes probes."""
    return jsonify({
        "status": "healthy",
        "uptime": "OK",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route("/info")
def info():
    """System info endpoint — useful for debugging deployments."""
    return jsonify({
        "app": "devops-cicd-showcase",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "os": platform.system()
    })


# ── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = ENVIRONMENT == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
