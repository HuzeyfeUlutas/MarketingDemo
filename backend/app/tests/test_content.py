"""İçerik (ContentItem) endpoint + durum akışı + yayınlama testleri."""

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.content import ContentItem, ContentStatus
from app.models.user import User
from app.services import content_service
from app.tests.conftest import auth_headers_for


def _create_content(client: TestClient, headers: dict, client_id: int, **kw) -> dict:
    payload = {"client_id": client_id, "title": "Yaz kampanyası", **kw}
    resp = client.post("/api/v1/content-items", headers=headers, json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_create_content_as_creator(
    client: TestClient, member_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "creator@agency.com", "creatorpass123")
    created = _create_content(
        client, headers, sample_client.id, platforms=["instagram", "x"]
    )
    assert created["status"] == "draft"
    assert created["platforms"] == ["instagram", "x"]
    assert created["created_by"]["id"] == member_user.id


def test_approval_flow(client: TestClient, admin_user: User, sample_client: Client):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    cid = _create_content(client, headers, sample_client.id)["id"]

    def set_status(status: str, **extra):
        return client.post(
            f"/api/v1/content-items/{cid}/status",
            headers=headers,
            json={"status": status, **extra},
        )

    # draft → pending_review → approved
    assert set_status("pending_review").status_code == 200
    appr = set_status("approved")
    assert appr.status_code == 200
    assert appr.json()["approved_by"]["id"] == admin_user.id

    # approved → scheduled (scheduled_at zorunlu)
    when = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    sched = set_status("scheduled", scheduled_at=when)
    assert sched.status_code == 200
    assert sched.json()["status"] == "scheduled"

    # scheduled → published
    pub = set_status("published")
    assert pub.status_code == 200
    assert pub.json()["published_at"] is not None


def test_invalid_transition_rejected(
    client: TestClient, admin_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    cid = _create_content(client, headers, sample_client.id)["id"]
    # draft → published doğrudan geçilemez
    resp = client.post(
        f"/api/v1/content-items/{cid}/status",
        headers=headers,
        json={"status": "published"},
    )
    assert resp.status_code == 400


def test_creator_cannot_approve(
    client: TestClient, member_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "creator@agency.com", "creatorpass123")
    cid = _create_content(client, headers, sample_client.id)["id"]
    client.post(
        f"/api/v1/content-items/{cid}/status",
        headers=headers,
        json={"status": "pending_review"},
    )
    # content_creator onaylayamaz (approved = onay yetkisi)
    resp = client.post(
        f"/api/v1/content-items/{cid}/status",
        headers=headers,
        json={"status": "approved"},
    )
    assert resp.status_code == 403


def test_scheduled_requires_time(
    client: TestClient, admin_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    cid = _create_content(client, headers, sample_client.id)["id"]
    client.post(
        f"/api/v1/content-items/{cid}/status",
        headers=headers,
        json={"status": "pending_review"},
    )
    client.post(
        f"/api/v1/content-items/{cid}/status", headers=headers, json={"status": "approved"}
    )
    # scheduled_at vermeden zamanlama → 400
    resp = client.post(
        f"/api/v1/content-items/{cid}/status", headers=headers, json={"status": "scheduled"}
    )
    assert resp.status_code == 400


def test_filter_by_client_and_status(
    client: TestClient, admin_user: User, sample_client: Client
):
    headers = auth_headers_for(client, "admin@agency.com", "adminpass123")
    _create_content(client, headers, sample_client.id)
    resp = client.get(
        f"/api/v1/content-items?client_id={sample_client.id}&status=draft", headers=headers
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_publish_due_scheduled_service(db_session: Session, sample_client: Client):
    """Zamanı geçmiş zamanlanmış içerik publish_due_scheduled ile yayınlanır."""
    past = datetime.now(UTC) - timedelta(minutes=5)
    future = datetime.now(UTC) + timedelta(days=1)
    db_session.add_all(
        [
            ContentItem(
                client_id=sample_client.id,
                title="Geçmiş",
                status=ContentStatus.scheduled,
                scheduled_at=past,
                platforms=[],
            ),
            ContentItem(
                client_id=sample_client.id,
                title="Gelecek",
                status=ContentStatus.scheduled,
                scheduled_at=future,
                platforms=[],
            ),
        ]
    )
    db_session.commit()

    published = content_service.publish_due_scheduled(db_session)
    assert published == 1
