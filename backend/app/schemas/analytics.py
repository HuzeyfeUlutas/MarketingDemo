"""Analytics & Report Pydantic şemaları."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.client import ClientMini
from app.schemas.user import UserSummary


class TimeseriesPoint(BaseModel):
    """Tek bir güne ait toplulaştırılmış metrikler."""

    date: date
    reach: int
    impressions: int
    engagement: int
    followers: int


class AnalyticsSummary(BaseModel):
    client_id: int
    period_days: int
    total_reach: int
    total_impressions: int
    total_engagement: int
    current_followers: int
    follower_growth: int
    engagement_rate: float  # yüzde
    timeseries: list[TimeseriesPoint]


class ReportCreate(BaseModel):
    client_id: int
    period_days: int = Field(default=30, ge=1, le=365)
    title: str | None = None


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    client: ClientMini | None = None
    title: str
    period_start: date
    period_end: date
    generated_by: UserSummary | None = None
    summary: dict
    generated_at: datetime
