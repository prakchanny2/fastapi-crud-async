
import json

import pytest

from app.api import events_crud as crud


def test_create_event(test_app, monkeypatch):
    payload = {
        "title": "Tech Conference",
        "city": "Phnom Penh",
        "price_usd": 25.5,
        "seats_left": 100
    }

    expected = {"id": 1, **payload}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/events/",
        content=json.dumps(payload)
    )

    assert response.status_code == 201
    assert response.json() == expected


def test_read_event(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "title": "Tech Conference",
        "city": "Phnom Penh",
        "price_usd": 25.5,
        "seats_left": 100
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/events/1/")

    assert response.status_code == 200
    assert response.json() == test_data


def test_read_missing_event(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/events/999/")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_read_all_events(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "title": "Tech Conference",
            "city": "Phnom Penh",
            "price_usd": 25.5,
            "seats_left": 100
        },
        {
            "id": 2,
            "title": "Music Festival",
            "city": "Siem Reap",
            "price_usd": 15.0,
            "seats_left": 200
        }
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/events/")

    assert response.status_code == 200
    assert response.json() == test_data


def test_update_event(test_app, monkeypatch):
    payload = {
        "title": "Updated Conference",
        "city": "Phnom Penh",
        "price_usd": 30.0,
        "seats_left": 80
    }

    async def mock_get(id):
        return True

    async def mock_put(id, payload):
        return id

    monkeypatch.setattr(crud, "get", mock_get)
    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/events/1/",
        content=json.dumps(payload)
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, **payload}


def test_update_event_invalid_data(test_app, monkeypatch):
    payload = {
        "title": "AB",
        "city": "Phnom Penh",
        "price_usd": 25.5,
        "seats_left": 100
    }

    response = test_app.put(
        "/events/1/",
        content=json.dumps(payload)
    )

    assert response.status_code == 422


def test_delete_event(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "title": "Tech Conference",
        "city": "Phnom Penh",
        "price_usd": 25.5,
        "seats_left": 100
    }

    async def mock_get(id):
        return test_data

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "get", mock_get)
    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/events/1/")

    assert response.status_code == 200
    assert response.json() == test_data
