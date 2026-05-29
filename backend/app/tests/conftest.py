"""Pytest fixtures: izole SQLite (in-memory) DB ve TestClient."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  (tüm tablolar metadata'ya kaydolsun)
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.services import user_service


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session: Session) -> User:
    return user_service.create_user(
        db_session,
        UserCreate(
            email="admin@agency.com",
            password="adminpass123",
            full_name="Admin User",
            role=UserRole.admin,
        ),
    )


@pytest.fixture
def member_user(db_session: Session) -> User:
    return user_service.create_user(
        db_session,
        UserCreate(
            email="creator@agency.com",
            password="creatorpass123",
            full_name="Creator User",
            role=UserRole.content_creator,
        ),
    )


def auth_headers_for(client: TestClient, email: str, password: str) -> dict[str, str]:
    """Login olup Authorization header döndürür."""
    resp = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
