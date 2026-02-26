import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Healthcare API" in response.json()["message"]


# Note: Full appointment tests will be added after database setup
# These are placeholder tests for Sprint 1
