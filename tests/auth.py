import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "full_name": "New User"
    }

    response = await client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient, test_user: dict):
    """Test registering a user with an existing username."""
    user_data = {
        "username": "testuser",  # Same username as test_user fixture
        "email": "another@example.com",
        "password": "password123",
        "full_name": "Another User"
    }

    response = await client.post("/api/auth/register", json=user_data)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user: dict):
    """Test user login."""
    response = await client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    response = await client.post(
        "/api/auth/login",
        data={"username": "nonexistent", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]