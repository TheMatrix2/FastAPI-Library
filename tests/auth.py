import pytest

def test_register_and_login(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "role": "reader"
    })
    assert response.status_code == 201

    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()