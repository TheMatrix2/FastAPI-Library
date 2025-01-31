import pytest

def test_create_book(client, db_session):
    token = "Bearer админский_токен"
    response = client.post("/books/", json={
        "title": "Тестовая книга",
        "description": "Описание книги",
        "publication_date": "2023-01-01",
        "genres": "Фантастика",
        "available_copies": 5
    }, headers={"Authorization": token})

    assert response.status_code == 201
    assert response.json()["title"] == "Тестовая книга"

def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)