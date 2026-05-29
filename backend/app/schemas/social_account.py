"""Sosyal hesap (mock) Pydantic şemaları."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.client import SocialPlatform


class SocialAccountBase(BaseModel):
    platform: SocialPlatform
    handle: str = Field(min_length=1, max_length=120)
    follower_count: int = Field(default=0, ge=0)
    avatar_url: str | None = Field(default=None, max_length=512)


class SocialAccountCreate(SocialAccountBase):
    pass


class SocialAccountUpdate(BaseModel):
    handle: str | None = Field(default=None, min_length=1, max_length=120)
    follower_count: int | None = Field(default=None, ge=0)
    avatar_url: str | None = Field(default=None, max_length=512)


class SocialAccountRead(SocialAccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    created_at: datetime
    updated_at: datetime
