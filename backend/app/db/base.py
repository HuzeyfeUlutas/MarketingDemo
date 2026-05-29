"""SQLAlchemy Declarative Base.

Tüm modeller bu Base'den türer. Alembic autogenerate'in tabloları görmesi
için modeller `app.models` içinde import edilmelidir.
"""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Tüm modellerin ortak temel sınıfı."""


class TimestampMixin:
    """created_at / updated_at alanlarını ekleyen yardımcı mixin."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
