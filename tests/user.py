import pytest

def test_get_readers(client):
    token = "Bearer админский_токен"
    response = client.get("/users/", headers={"Authorization": token})
    assert response.status_code == 200
    assert isinstance(response.json(), list)