import pytest

def test_create_author(client):
    token = "Bearer админский_токен"
    response = client.post("/authors/", json={
        "name": "Айзек Азимов",
        "biography": "Писатель-фантаст",
        "birth_date": "1920-01-02"
    }, headers={"Authorization": token})

    assert response.status_code == 201
    assert response.json()["name"] == "Айзек Азимов"