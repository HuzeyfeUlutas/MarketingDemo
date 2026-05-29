"""Müşteri (Client) ve sosyal hesap endpoint testleri."""

from fastapi.testclient import TestClient

from app.models.user import User
from app.tests.conftest import auth_headers_for


def _create_client(client: TestClient, headers: dict[str, str], **overrides) -> dict:
    payload = {"name": "Acme Corp", "industry": "Retail", **overrides}
    resp = client.post("/api/v1/clients", headers=headers, json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_member_can_list_but_not_create(client: TestClient, member_user: User):
    headers = auth_headers_for(client, "creator@agency.com", "creatorpass123")
    # content_creator görüntüleyebilir
    assert client.get("/api/v1/clients", headers=headers).status_code == 200
    # ama oluşturamaz (admin/manager gerekir)
    resp = client.post("/api/v1/clients", headers=headers, json={"name": "X"})
    assert resp.status_code == 403


def test_admin_crud_client(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    created = _create_client(client, headers)
    cid = created["id"]
    assert created["status"] == "active"
    assert created["social_accounts"] == []

    # güncelle
    upd = client.patch(
        f"/api/v1/clients/{cid}", headers=headers, json={"status": "paused"}
    )
    assert upd.status_code == 200
    assert upd.json()["status"] == "paused"

    # sil
    assert client.delete(f"/api/v1/clients/{cid}", headers=headers).status_code == 204
    assert client.get(f"/api/v1/clients/{cid}", headers=headers).status_code == 404


def test_assign_manager(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    # admin atanabilir yönetici listesinde görünür
    managers = client.get("/api/v1/clients/assignable-managers", headers=headers)
    assert managers.status_code == 200
    assert any(m["id"] == admin_user.id for m in managers.json())

    created = _create_client(client, headers, manager_id=admin_user.id)
    assert created["manager"]["id"] == admin_user.id


def test_invalid_manager_rejected(client: TestClient, admin_user: User, member_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    # content_creator manager olamaz
    resp = client.post(
        "/api/v1/clients",
        headers=headers,
        json={"name": "Bad", "manager_id": member_user.id},
    )
    assert resp.status_code == 400


def test_social_accounts_flow(client: TestClient, admin_user: User):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    cid = _create_client(client, headers)["id"]

    # ekle (follower_count verilmezse mock üretilir)
    add = client.post(
        f"/api/v1/clients/{cid}/social-accounts",
        headers=headers,
        json={"platform": "instagram", "handle": "@acme"},
    )
    assert add.status_code == 201
    acc = add.json()
    assert acc["platform"] == "instagram"
    assert acc["follower_count"] > 0

    # client detayında görünür
    detail = client.get(f"/api/v1/clients/{cid}", headers=headers).json()
    assert len(detail["social_accounts"]) == 1

    # güncelle
    upd = client.patch(
        f"/api/v1/clients/{cid}/social-accounts/{acc['id']}",
        headers=headers,
        json={"follower_count": 1234},
    )
    assert upd.status_code == 200
    assert upd.json()["follower_count"] == 1234

    # sil
    assert (
        client.delete(
            f"/api/v1/clients/{cid}/social-accounts/{acc['id']}", headers=headers
        ).status_code
        == 204
    )
