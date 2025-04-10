from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_table():
    response = client.post("/tables/", json={"name": "Table 2", "seats": 4, "location": "Terrace"})
    assert response.status_code == 200
    assert response.json()["name"] == "Table 2"


def test_delete_table():
    # Создаем столик
    response = client.post("/tables/", json={"name": "Table 3", "seats": 4, "location": "Garden"})
    table_id = response.json()["id"]

    # Удаляем столик
    response = client.delete(f"/tables/{table_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Table deleted"


def test_delete_nonexistent_table():
    response = client.delete("/tables/9999")  # Не существующий ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Table not found"
