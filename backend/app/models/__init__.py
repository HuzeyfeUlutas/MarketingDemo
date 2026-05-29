"""SQLAlchemy modelleri.

Alembic'in (autogenerate) ve test kurulumunun (create_all) tüm tabloları
görebilmesi için modeller buradan import edilir.
"""

from app.models.client import Client, ClientStatus, SocialAccount, SocialPlatform
from app.models.content import Asset, AssetType, ContentItem, ContentStatus
from app.models.user import User, UserRole

__all__ = [
    "User",
    "UserRole",
    "Client",
    "ClientStatus",
    "SocialAccount",
    "SocialPlatform",
    "ContentItem",
    "ContentStatus",
    "Asset",
    "AssetType",
]
