import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_reservation():
    response = client.post("/reservations/", json={
        "customer_name": "John Doe",
        "table_id": 1,
        "reservation_time": "2023-01-01T12:00:00",
        "duration_minutes": 60
    })
    assert response.status_code == 200
    assert response.json()["customer_name"] == "John Doe"


def test_conflicting_reservation():
    # Создаем первую бронь
    response = client.post("/reservations/", json={
        "customer_name": "John Doe",
        "table_id": 1,
        "reservation_time": "2023-01-01T12:00:00",
        "duration_minutes": 60
    })
    assert response.status_code == 200

    # Пытаемся создать конфликтующую бронь
    response = client.post("/reservations/", json={
        "customer_name": "Jane Doe",
        "table_id": 1,
        "reservation_time": "2023-01-01T12:30:00",  # Конфликт с первой бронью
        "duration_minutes": 30
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Time slot is already booked for this table."


def test_delete_reservation():
    # Создаем бронь
    response = client.post("/reservations/", json={
        "customer_name": "Emily Doe",
        "table_id": 1,
        "reservation_time": "2023-01-01T13:00:00",
        "duration_minutes": 30
    })
    reservation_id = response.json()["id"]

    # Удаляем бронь
    response = client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Reservation deleted"


def test_delete_nonexistent_reservation():
    response = client.delete("/reservations/9999")  # Не существующий ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"
