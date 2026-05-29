"""Analytics iş mantığı: mock metrik üretimi, toplulaştırma, rapor."""

import random
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.analytics import AnalyticsSnapshot, Report
from app.models.client import Client
from app.models.user import User


def _existing_dates(db: Session, client_id: int, account_id: int | None) -> set[date]:
    stmt = select(AnalyticsSnapshot.date).where(
        AnalyticsSnapshot.client_id == client_id,
        AnalyticsSnapshot.social_account_id.is_(account_id)
        if account_id is None
        else AnalyticsSnapshot.social_account_id == account_id,
    )
    return set(db.scalars(stmt))


def generate_snapshots_for_client(db: Session, client: Client, days: int = 30) -> int:
    """Müşteri için son `days` güne ait MOCK metrikleri üretir (mevcut günleri atlar).

    Her sosyal hesap için ayrı seri; hesap yoksa client geneli (account_id=None).
    Takipçi sayısı yukarı yönlü rastgele yürüyüşle (trend) simüle edilir.
    """
    accounts: list = list(client.social_accounts) or [None]
    today = date.today()
    created = 0

    for account in accounts:
        account_id = account.id if account is not None else None
        existing = _existing_dates(db, client.id, account_id)

        base = account.follower_count if account is not None else random.randint(2_000, 80_000)
        # Serinin başlangıç takipçisi (geçmişe doğru daha düşük).
        followers = max(200, base - days * random.randint(10, 60))

        for offset in range(days, -1, -1):
            day = today - timedelta(days=offset)
            followers += random.randint(-30, 150)  # genel yükseliş trendi
            if day in existing:
                continue
            impressions = random.randint(800, 25_000)
            reach = int(impressions * random.uniform(0.5, 0.9))
            engagement = int(impressions * random.uniform(0.01, 0.08))
            db.add(
                AnalyticsSnapshot(
                    client_id=client.id,
                    social_account_id=account_id,
                    date=day,
                    reach=reach,
                    impressions=impressions,
                    engagement=engagement,
                    followers=max(0, followers),
                )
            )
            created += 1

    if created:
        db.commit()
    return created


def get_timeseries(db: Session, client_id: int, days: int = 30) -> list[dict]:
    """Tarihe göre toplulaştırılmış metrik serisi (hesaplar toplanır)."""
    since = date.today() - timedelta(days=days)
    stmt = (
        select(AnalyticsSnapshot)
        .where(AnalyticsSnapshot.client_id == client_id, AnalyticsSnapshot.date >= since)
        .order_by(AnalyticsSnapshot.date)
    )
    by_date: dict[date, dict] = {}
    for s in db.scalars(stmt):
        agg = by_date.setdefault(
            s.date, {"date": s.date, "reach": 0, "impressions": 0, "engagement": 0, "followers": 0}
        )
        agg["reach"] += s.reach
        agg["impressions"] += s.impressions
        agg["engagement"] += s.engagement
        agg["followers"] += s.followers
    return [by_date[d] for d in sorted(by_date)]


def get_summary(db: Session, client_id: int, days: int = 30) -> dict:
    """Dönem özeti: toplamlar, takipçi büyümesi, etkileşim oranı."""
    ts = get_timeseries(db, client_id, days)
    total_reach = sum(p["reach"] for p in ts)
    total_impressions = sum(p["impressions"] for p in ts)
    total_engagement = sum(p["engagement"] for p in ts)
    current_followers = ts[-1]["followers"] if ts else 0
    first_followers = ts[0]["followers"] if ts else 0
    engagement_rate = (
        round(total_engagement / total_impressions * 100, 2) if total_impressions else 0.0
    )
    return {
        "client_id": client_id,
        "period_days": days,
        "total_reach": total_reach,
        "total_impressions": total_impressions,
        "total_engagement": total_engagement,
        "current_followers": current_followers,
        "follower_growth": current_followers - first_followers,
        "engagement_rate": engagement_rate,
        "timeseries": ts,
    }


def create_report(
    db: Session, client: Client, days: int, generated_by: User, title: str | None = None
) -> Report:
    summary = get_summary(db, client.id, days)
    # timeseries'i rapora gömmeyelim; özet metrikleri saklayalım.
    summary_metrics = {k: v for k, v in summary.items() if k != "timeseries"}
    end = date.today()
    report = Report(
        client_id=client.id,
        title=title or f"{client.name} — {days} günlük performans raporu",
        period_start=end - timedelta(days=days),
        period_end=end,
        generated_by_id=generated_by.id,
        summary=summary_metrics,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def list_reports(db: Session, client_id: int | None = None) -> list[Report]:
    stmt = select(Report).order_by(Report.generated_at.desc())
    if client_id is not None:
        stmt = stmt.where(Report.client_id == client_id)
    return list(db.scalars(stmt))


def get_report(db: Session, report_id: int) -> Report | None:
    return db.get(Report, report_id)


def generate_daily_for_all(db: Session) -> int:
    """Tüm müşteriler için bugünün snapshot'ını üretir (Celery beat tarafından)."""
    total = 0
    for client in db.scalars(select(Client)):
        total += generate_snapshots_for_client(db, client, days=0)
    return total
