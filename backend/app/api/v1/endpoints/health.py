"""Sağlık kontrolü (health check) endpoint'i."""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", summary="Servis sağlık kontrolü")
def health() -> dict[str, str]:
    """Servisin ayakta olduğunu doğrular. Monitoring/uptime için kullanılır."""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "project": settings.PROJECT_NAME,
    }
