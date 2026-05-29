"""İçerik (ContentItem) ve medya (Asset) Pydantic şemaları."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.client import SocialPlatform
from app.models.content import AssetType, ContentStatus
from app.schemas.client import ClientMini
from app.schemas.user import UserSummary


class AssetCreate(BaseModel):
    type: AssetType
    url: str = Field(min_length=1, max_length=1024)
    filename: str | None = Field(default=None, max_length=255)


class AssetRead(AssetCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content_item_id: int


class ContentItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = ""
    platforms: list[SocialPlatform] = []
    scheduled_at: datetime | None = None


class ContentItemCreate(ContentItemBase):
    client_id: int


class ContentItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    body: str | None = None
    platforms: list[SocialPlatform] | None = None
    scheduled_at: datetime | None = None


class ContentStatusUpdate(BaseModel):
    status: ContentStatus
    # scheduled durumuna geçerken zorunlu.
    scheduled_at: datetime | None = None


class ContentItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    client: ClientMini | None = None
    title: str
    body: str
    platforms: list[str]
    status: ContentStatus
    scheduled_at: datetime | None
    published_at: datetime | None
    created_by: UserSummary | None = None
    approved_by: UserSummary | None = None
    assets: list[AssetRead] = []
    created_at: datetime
    updated_at: datetime
