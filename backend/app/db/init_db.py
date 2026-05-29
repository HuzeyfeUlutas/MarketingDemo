"""İlk admin (superuser) seed işlemi.

Çalıştırma:  python -m app.db.init_db
Kimlik bilgileri ortam değişkenlerinden okunur (repoda parola YOK):
    FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_PASSWORD, FIRST_SUPERUSER_NAME
"""

import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import UserRole
from app.schemas.user import UserCreate
from app.services import user_service

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    if not settings.FIRST_SUPERUSER_EMAIL or not settings.FIRST_SUPERUSER_PASSWORD:
        logger.info("FIRST_SUPERUSER_* tanımlı değil; admin seed atlandı.")
        return

    existing = user_service.get_user_by_email(db, settings.FIRST_SUPERUSER_EMAIL)
    if existing:
        logger.info("Admin zaten mevcut: %s", settings.FIRST_SUPERUSER_EMAIL)
        return

    user_service.create_user(
        db,
        UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_SUPERUSER_NAME,
            role=UserRole.admin,
            is_active=True,
        ),
    )
    logger.info("Admin oluşturuldu: %s", settings.FIRST_SUPERUSER_EMAIL)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
