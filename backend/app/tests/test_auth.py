"""Auth akışı testleri."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.tests.conftest import auth_headers_for


def test_login_success(client: TestClient, admin_user: User):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@agency.com", "password": "adminpass123"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"] and body["refresh_token"]
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, admin_user: User):
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@agency.com", "password": "yanlis"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client: TestClient):
    assert client.get("/api/v1/auth/me").status_code == 401


def test_me_returns_current_user(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "admin@agency.com"
    assert resp.json()["role"] == "admin"


def test_refresh_token(client: TestClient, admin_user: User):
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@agency.com", "password": "adminpass123"},
    )
    refresh_token = login.json()["refresh_token"]
    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_inactive_user_cannot_login(client: TestClient, db_session: Session, member_user: User):
    member_user.is_active = False
    db_session.commit()
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "creator@agency.com", "password": "creatorpass123"},
    )
    assert resp.status_code == 403
