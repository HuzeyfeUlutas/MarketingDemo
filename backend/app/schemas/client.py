"""Müşteri (Client) Pydantic şemaları."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.client import ClientStatus
from app.schemas.social_account import SocialAccountRead
from app.schemas.user import UserSummary


class ClientBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    industry: str | None = Field(default=None, max_length=120)
    website: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    status: ClientStatus = ClientStatus.active
    manager_id: int | None = None


class ClientCreate(ClientBase):
    pass


class ClientMini(BaseModel):
    """Diğer kaynaklarda gömülü gösterim için hafif müşteri bilgisi."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    industry: str | None = Field(default=None, max_length=120)
    website: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    status: ClientStatus | None = None
    manager_id: int | None = None


class ClientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    industry: str | None
    website: str | None
    notes: str | None
    status: ClientStatus
    manager_id: int | None
    manager: UserSummary | None = None
    social_accounts: list[SocialAccountRead] = []
    created_at: datetime
    updated_at: datetime
