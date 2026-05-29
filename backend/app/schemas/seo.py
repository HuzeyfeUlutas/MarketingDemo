"""SEO Pydantic şemaları."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class RankPoint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    position: int


class KeywordCreate(BaseModel):
    client_id: int
    term: str = Field(min_length=1, max_length=255)
    target_url: str | None = Field(default=None, max_length=512)
    search_volume: int | None = Field(default=None, ge=0)


class KeywordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    term: str
    target_url: str | None
    search_volume: int
    rankings: list[RankPoint] = []
    created_at: datetime


class SiteAuditRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    date: date
    score: int
    issues: list[dict]
    created_at: datetime


class BacklinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    source_url: str
    authority: int
    discovered_at: datetime
