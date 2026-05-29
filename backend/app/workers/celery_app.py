"""Celery uygulaması ve task'lar.

`publish_scheduled_content`: zamanı gelen (scheduled_at <= now) zamanlanmış
içerikleri (mock) yayınlar. Celery beat ile periyodik çalışır.
"""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "agency",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "publish-scheduled-content-every-minute": {
            "task": "tasks.publish_scheduled_content",
            "schedule": 60.0,
        },
    },
)


@celery_app.task(name="tasks.ping")
def ping() -> str:
    """Worker'ın çalıştığını doğrulayan basit örnek task."""
    return "pong"


@celery_app.task(name="tasks.publish_scheduled_content")
def publish_scheduled_content() -> int:
    """Zamanı gelmiş zamanlanmış içerikleri yayınlar. Yayınlanan sayıyı döner."""
    # Import burada: Celery worker'ı uygulama modüllerini geç yüklesin.
    from app.db.session import SessionLocal
    from app.services import content_service

    db = SessionLocal()
    try:
        return content_service.publish_due_scheduled(db)
    finally:
        db.close()
