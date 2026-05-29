"""İçerik (ContentItem) ve medya (Asset) modelleri + içerik durum akışı.

Durum akışı (status):
    draft → pending_review → approved → scheduled → published
Geri dönüşler: pending_review→draft, approved→draft, scheduled→approved.
Zamanlanmış içerik, Celery task'ı ile zamanı gelince (mock) yayınlanır.
"""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ContentStatus(StrEnum):
    draft = "draft"
    pending_review = "pending_review"
    approved = "approved"
    scheduled = "scheduled"
    published = "published"


class AssetType(StrEnum):
    image = "image"
    video = "video"
    document = "document"
    link = "link"


class ContentItem(Base, TimestampMixin):
    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", nullable=False)
    # Hedef platformlar (SocialPlatform değerleri listesi) — JSON olarak saklanır.
    platforms: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[ContentStatus] = mapped_column(
        Enum(ContentStatus, native_enum=False, length=20),
        default=ContentStatus.draft,
        nullable=False,
        index=True,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    client = relationship("Client", lazy="joined")
    created_by = relationship("User", foreign_keys=[created_by_id], lazy="joined")
    approved_by = relationship("User", foreign_keys=[approved_by_id], lazy="joined")
    assets = relationship(
        "Asset", back_populates="content_item", cascade="all, delete-orphan", lazy="selectin"
    )


class Asset(Base, TimestampMixin):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    content_item_id: Mapped[int] = mapped_column(
        ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, native_enum=False, length=16), nullable=False
    )
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    filename: Mapped[str | None] = mapped_column(String(255), nullable=True)

    content_item = relationship("ContentItem", back_populates="assets")
