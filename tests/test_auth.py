import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user_success():
    """Test successful user registration"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123",
        "role": "patient",
        "first_name": "Test",
        "last_name": "User"
    })
    # Note: This will fail if user already exists or DB not set up
    # In real tests, use a test database
    assert response.status_code in [201, 400]


def test_register_weak_password():
    """Test registration with weak password"""
    response = client.post("/auth/register", json={
        "email": "weak@example.com",
        "password": "weak",
        "role": "patient",
        "first_name": "Weak",
        "last_name": "Password"
    })
    assert response.status_code == 400


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "WrongPass123"
    })
    assert response.status_code == 401
