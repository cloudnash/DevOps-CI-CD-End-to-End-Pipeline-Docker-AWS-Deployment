"""
Unit Tests for DevOps Showcase App
Run with: pytest app/tests/test_app.py -v
"""
from app import app
import pytest
import sys
import os


# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))




@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
# ── Tests ────────────────────────────────────────────────────────────────────

class TestHomeRoute:
    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_json(self, client):
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_home_has_message(self, client):
        data = client.get("/").get_json()
        assert "message" in data
        assert "version" in data

class TestHealthRoute:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_healthy(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "healthy"

class TestInfoRoute:
    def test_info_returns_200(self, client):
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_has_required_fields(self, client):
        data = client.get("/info").get_json()
        required_fields = ["app", "version", "environment", "python_version"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
