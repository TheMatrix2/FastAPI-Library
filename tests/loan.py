import pytest

def test_create_loan(client):
    token = "Bearer токен_читателя"
    response = client.post("/loans/", json={
        "book_id": 1,
        "user_id": 2,
        "return_date": "2024-02-10"
    }, headers={"Authorization": token})

    assert response.status_code == 201