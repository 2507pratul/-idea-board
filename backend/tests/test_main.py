
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

import main


class FakeCursor:
    def __init__(self, rows=None, row=None):
        self.rows = rows or []
        self.row = row

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.row


class FakeConnection:
    def __init__(self, storage):
        self.storage = storage

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def execute(self, query, params=None):
        query = " ".join(query.split()).upper()

        if query.startswith("CREATE TABLE"):
            return FakeCursor()

        if query.startswith("SELECT"):
            rows = sorted(
                self.storage,
                key=lambda item: item[0],
                reverse=True
            )
            return FakeCursor(rows=rows)

        if query.startswith("INSERT"):
            content = params[0]
            new_id = max(
                [item[0] for item in self.storage],
                default=0
            ) + 1

            row = (
                new_id,
                content,
                datetime.now(timezone.utc)
            )
            self.storage.append(row)
            return FakeCursor(row=row)

        if query.startswith("UPDATE"):
            content, idea_id = params

            for index, item in enumerate(self.storage):
                if item[0] == idea_id:
                    row = (item[0], content, item[2])
                    self.storage[index] = row
                    return FakeCursor(row=row)

            return FakeCursor()

        if query.startswith("DELETE"):
            idea_id = params[0]

            for index, item in enumerate(self.storage):
                if item[0] == idea_id:
                    self.storage.pop(index)
                    return FakeCursor(row=(idea_id,))

            return FakeCursor()

        raise NotImplementedError(f"Unexpected query: {query}")


@pytest.fixture
def client(monkeypatch):
    storage = []

    monkeypatch.setattr(
        main,
        "get_connection",
        lambda: FakeConnection(storage)
    )

    with TestClient(main.app) as test_client:
        yield test_client


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Idea Board API"


def test_get_ideas(client):
    response = client.get("/api/ideas")

    assert response.status_code == 200
    assert response.json() == []


def test_create_idea(client):
    response = client.post(
        "/api/ideas",
        json={"content": "Learn Docker"}
    )

    assert response.status_code == 201
    assert response.json()["content"] == "Learn Docker"
    assert "id" in response.json()


def test_create_empty_idea(client):
    response = client.post(
        "/api/ideas",
        json={"content": "   "}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Idea content cannot be empty"


def test_update_idea(client):
    created = client.post(
        "/api/ideas",
        json={"content": "Learn Python"}
    )

    idea_id = created.json()["id"]

    response = client.put(
        f"/api/ideas/{idea_id}",
        json={"content": "Learn FastAPI"}
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Learn FastAPI"


def test_update_missing_idea(client):
    response = client.put(
        "/api/ideas/999",
        json={"content": "Updated idea"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Idea not found"


def test_delete_idea(client):
    created = client.post(
        "/api/ideas",
        json={"content": "Learn Kubernetes"}
    )

    idea_id = created.json()["id"]

    response = client.delete(f"/api/ideas/{idea_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Idea deleted successfully"


def test_delete_missing_idea(client):
    response = client.delete("/api/ideas/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Idea not found"
