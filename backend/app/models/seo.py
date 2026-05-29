"""SEO modelleri: Keyword, RankTracking, SiteAudit, Backlink.

İlk fazda tüm SEO verileri MOCK'tur (gerçek arama motoru/SEO API yerine
gerçekçi rastgele değerler — bkz. services/seo_service.py).
"""

from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class IssueSeverity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class Keyword(Base, TimestampMixin):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    term: Mapped[str] = mapped_column(String(255), nullable=False)
    target_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    search_volume: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    rankings = relationship(
        "RankTracking",
        back_populates="keyword",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="RankTracking.date",
    )


class RankTracking(Base, TimestampMixin):
    __tablename__ = "rank_trackings"

    id: Mapped[int] = mapped_column(primary_key=True)
    keyword_id: Mapped[int] = mapped_column(
        ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 = en iyi

    keyword = relationship("Keyword", back_populates="rankings")


class SiteAudit(Base, TimestampMixin):
    __tablename__ = "site_audits"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-100
    # [{ "title": str, "severity": "low|medium|high" }, ...]
    issues: Mapped[list] = mapped_column(JSON, default=list, nullable=False)


class Backlink(Base, TimestampMixin):
    __tablename__ = "backlinks"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_url: Mapped[str] = mapped_column(String(512), nullable=False)
    authority: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # 0-100
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
