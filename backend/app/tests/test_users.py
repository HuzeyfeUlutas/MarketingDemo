"""Kullanıcı/ekip yönetimi endpoint testleri (rol tabanlı yetki)."""

from fastapi.testclient import TestClient

from app.models.user import User
from app.tests.conftest import auth_headers_for


def test_member_cannot_list_users(client: TestClient, member_user: User):
    headers = auth_headers_for(client, "creator@agency.com", "creatorpass123")
    assert client.get("/api/v1/users", headers=headers).status_code == 403


def test_admin_can_list_users(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    resp = client.get("/api/v1/users", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_admin_creates_user(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    resp = client.post(
        "/api/v1/users",
        headers=headers,
        json={
            "email": "analyst@agency.com",
            "full_name": "Analyst One",
            "role": "analyst",
            "password": "analystpass123",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["email"] == "analyst@agency.com"
    assert "password" not in resp.json()


def test_duplicate_email_conflict(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    payload = {
        "email": "admin@agency.com",
        "full_name": "Dup",
        "role": "manager",
        "password": "somepass123",
    }
    assert client.post("/api/v1/users", headers=headers, json=payload).status_code == 409


def test_admin_updates_and_deletes_user(client: TestClient, admin_user: User, member_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")

    upd = client.patch(
        f"/api/v1/users/{member_user.id}",
        headers=headers,
        json={"role": "manager", "is_active": False},
    )
    assert upd.status_code == 200
    assert upd.json()["role"] == "manager"
    assert upd.json()["is_active"] is False

    dele = client.delete(f"/api/v1/users/{member_user.id}", headers=headers)
    assert dele.status_code == 204


def test_admin_cannot_delete_self(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    resp = client.delete(f"/api/v1/users/{admin_user.id}", headers=headers)
    assert resp.status_code == 400
