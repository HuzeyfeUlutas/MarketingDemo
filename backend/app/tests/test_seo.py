"""SEO Araçları endpoint testleri."""

from fastapi.testclient import TestClient

from app.models.client import Client
from app.models.user import User
from app.tests.conftest import auth_headers_for


def test_view_allowed_edit_requires_seo_role(
    client: TestClient, member_user: User, sample_client: Client
):
    # content_creator görüntüleyebilir
    headers = auth_headers_for(client, "creator@agency.com", "creatorpass123")
    view = client.get(f"/api/v1/seo/keywords?client_id={sample_client.id}", headers=headers)
    assert view.status_code == 200
    # ama anahtar kelime ekleyemez (SEO yetkisi yok)
    resp = client.post(
        "/api/v1/seo/keywords",
        headers=headers,
        json={"client_id": sample_client.id, "term": "ayakkabı"},
    )
    assert resp.status_code == 403


def test_create_keyword_with_rank_history(
    client: TestClient, admin_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    resp = client.post(
        "/api/v1/seo/keywords",
        headers=headers,
        json={"client_id": sample_client.id, "term": "spor ayakkabı", "search_volume": 5000},
    )
    assert resp.status_code == 201
    kw = resp.json()
    assert kw["term"] == "spor ayakkabı"
    assert kw["search_volume"] == 5000
    # 0..30 dahil = 31 nokta sıralama geçmişi
    assert len(kw["rankings"]) == 31
    assert all(1 <= p["position"] <= 100 for p in kw["rankings"])


def test_delete_keyword(client: TestClient, admin_user: User, sample_client: Client):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    kid = client.post(
        "/api/v1/seo/keywords",
        headers=headers,
        json={"client_id": sample_client.id, "term": "x"},
    ).json()["id"]
    assert client.delete(f"/api/v1/seo/keywords/{kid}", headers=headers).status_code == 204


def test_site_audit(client: TestClient, admin_user: User, sample_client: Client):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    run = client.post(
        f"/api/v1/seo/site-audits?client_id={sample_client.id}", headers=headers
    )
    assert run.status_code == 201
    audit = run.json()
    assert 0 <= audit["score"] <= 100
    assert len(audit["issues"]) >= 1
    assert "severity" in audit["issues"][0]

    listing = client.get(
        f"/api/v1/seo/site-audits?client_id={sample_client.id}", headers=headers
    )
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_backlinks(client: TestClient, admin_user: User, sample_client: Client):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    gen = client.post(
        f"/api/v1/seo/backlinks/generate?client_id={sample_client.id}&count=5", headers=headers
    )
    assert gen.status_code == 200
    assert gen.json()["created"] == 5

    listing = client.get(
        f"/api/v1/seo/backlinks?client_id={sample_client.id}", headers=headers
    ).json()
    assert len(listing) == 5
    # otorite azalan sıralı
    authorities = [b["authority"] for b in listing]
    assert authorities == sorted(authorities, reverse=True)
