"""Celery uygulaması ve örnek task.

İleride zamanlanmış gönderi yayınlama, mock analytics üretimi ve SEO
taramaları gibi arka plan işleri burada tanımlanacak.
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
)


@celery_app.task(name="tasks.ping")
def ping() -> str:
    """Worker'ın çalıştığını doğrulayan basit örnek task."""
    return "pong"
