"""Müşteri (Client) ve ona bağlı sosyal medya hesabı modelleri.

İlk fazda sosyal hesaplar MOCK'tur: gerçek token/erişim yoktur, yalnızca
görüntülenecek meta veriler (handle, takipçi sayısı, avatar) tutulur.
"""

from enum import StrEnum

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ClientStatus(StrEnum):
    active = "active"
    paused = "paused"
    archived = "archived"


class SocialPlatform(StrEnum):
    instagram = "instagram"
    facebook = "facebook"
    x = "x"
    linkedin = "linkedin"
    tiktok = "tiktok"
    youtube = "youtube"


class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    industry: Mapped[str | None] = mapped_column(String(120), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ClientStatus] = mapped_column(
        Enum(ClientStatus, native_enum=False, length=16),
        default=ClientStatus.active,
        nullable=False,
    )
    # Sorumlu hesap yöneticisi (manager). Kullanıcı silinirse NULL'a düşer.
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    manager = relationship("User", lazy="joined")
    social_accounts = relationship(
        "SocialAccount",
        back_populates="client",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class SocialAccount(Base, TimestampMixin):
    __tablename__ = "social_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    platform: Mapped[SocialPlatform] = mapped_column(
        Enum(SocialPlatform, native_enum=False, length=16), nullable=False
    )
    handle: Mapped[str] = mapped_column(String(120), nullable=False)
    follower_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    client = relationship("Client", back_populates="social_accounts")
