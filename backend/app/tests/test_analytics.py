"""Analytics & Raporlama endpoint/servis testleri."""

from fastapi.testclient import TestClient

from app.models.client import Client
from app.models.user import User
from app.services import analytics_service
from app.tests.conftest import auth_headers_for


def test_generate_requires_manager(
    client: TestClient, member_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "creator@agency.com", "creatorpass123")
    resp = client.post(
        f"/api/v1/analytics/generate?client_id={sample_client.id}&days=10", headers=headers
    )
    assert resp.status_code == 403


def test_generate_and_summary(client: TestClient, admin_user: User, sample_client: Client):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    gen = client.post(
        f"/api/v1/analytics/generate?client_id={sample_client.id}&days=14", headers=headers
    )
    assert gen.status_code == 200
    # 0..14 dahil -> 15 gün
    assert gen.json()["created"] == 15

    summ = client.get(
        f"/api/v1/analytics/summary?client_id={sample_client.id}&days=14", headers=headers
    )
    assert summ.status_code == 200
    body = summ.json()
    assert body["total_impressions"] > 0
    assert len(body["timeseries"]) == 15
    assert "engagement_rate" in body


def test_generate_idempotent_per_day(
    client: TestClient, admin_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    first = client.post(
        f"/api/v1/analytics/generate?client_id={sample_client.id}&days=5", headers=headers
    ).json()["created"]
    second = client.post(
        f"/api/v1/analytics/generate?client_id={sample_client.id}&days=5", headers=headers
    ).json()["created"]
    assert first == 6
    assert second == 0  # aynı günler tekrar üretilmez


def test_report_flow(client: TestClient, admin_user: User, sample_client: Client):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    client.post(
        f"/api/v1/analytics/generate?client_id={sample_client.id}&days=10", headers=headers
    )
    created = client.post(
        "/api/v1/analytics/reports",
        headers=headers,
        json={"client_id": sample_client.id, "period_days": 10},
    )
    assert created.status_code == 201
    report = created.json()
    assert report["summary"]["total_reach"] >= 0
    assert report["generated_by"]["id"] == admin_user.id

    listing = client.get(
        f"/api/v1/analytics/reports?client_id={sample_client.id}", headers=headers
    )
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_summary_service_growth(db_session, sample_client: Client):
    analytics_service.generate_snapshots_for_client(db_session, sample_client, days=20)
    summary = analytics_service.get_summary(db_session, sample_client.id, days=20)
    assert summary["current_followers"] >= 0
    assert summary["period_days"] == 20
