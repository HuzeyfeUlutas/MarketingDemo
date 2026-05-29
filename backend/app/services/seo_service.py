"""SEO iş mantığı: anahtar kelime/sıralama, site denetimi, backlink (MOCK)."""

import random
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.seo import Backlink, Keyword, RankTracking, SiteAudit
from app.schemas.seo import KeywordCreate

# Mock site denetimi sorun havuzu.
_ISSUE_POOL = [
    {"title": "Eksik meta açıklamaları", "severity": "medium"},
    {"title": "Yavaş sayfa yükleme süresi", "severity": "high"},
    {"title": "Kırık bağlantılar (404)", "severity": "high"},
    {"title": "Alt etiketi olmayan görseller", "severity": "low"},
    {"title": "Yinelenen başlık etiketleri", "severity": "medium"},
    {"title": "Mobil uyumluluk uyarıları", "severity": "medium"},
    {"title": "HTTPS yönlendirme eksikliği", "severity": "high"},
    {"title": "Zayıf iç bağlantı yapısı", "severity": "low"},
]

_BACKLINK_DOMAINS = [
    "techblog.example",
    "news.example",
    "review.example",
    "forum.example",
    "partner.example",
    "directory.example",
]


# ---- Keyword & sıralama ----


def list_keywords(db: Session, client_id: int) -> list[Keyword]:
    stmt = select(Keyword).where(Keyword.client_id == client_id).order_by(Keyword.term)
    return list(db.scalars(stmt))


def get_keyword(db: Session, keyword_id: int) -> Keyword | None:
    return db.get(Keyword, keyword_id)


def create_keyword(db: Session, data: KeywordCreate, history_days: int = 30) -> Keyword:
    keyword = Keyword(
        client_id=data.client_id,
        term=data.term,
        target_url=data.target_url,
        search_volume=data.search_volume
        if data.search_volume is not None
        else random.randint(100, 20_000),
    )
    db.add(keyword)
    db.flush()  # id almak için

    # Mock sıralama geçmişi: 1..100 arası, hafif iyileşme trendi (düşen pozisyon).
    position = random.randint(20, 80)
    today = date.today()
    for offset in range(history_days, -1, -1):
        position = max(1, min(100, position + random.randint(-3, 2)))
        db.add(
            RankTracking(
                keyword_id=keyword.id, date=today - timedelta(days=offset), position=position
            )
        )

    db.commit()
    db.refresh(keyword)
    return keyword


def delete_keyword(db: Session, keyword: Keyword) -> None:
    db.delete(keyword)
    db.commit()


# ---- Site denetimi ----


def list_site_audits(db: Session, client_id: int) -> list[SiteAudit]:
    stmt = (
        select(SiteAudit)
        .where(SiteAudit.client_id == client_id)
        .order_by(SiteAudit.date.desc())
    )
    return list(db.scalars(stmt))


def run_site_audit(db: Session, client_id: int) -> SiteAudit:
    issues = random.sample(_ISSUE_POOL, k=random.randint(2, 5))
    # Skor: yüksek önem arttıkça düşer.
    penalty = sum({"low": 3, "medium": 7, "high": 14}[i["severity"]] for i in issues)
    score = max(40, 100 - penalty - random.randint(0, 8))
    audit = SiteAudit(client_id=client_id, date=date.today(), score=score, issues=issues)
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


# ---- Backlink ----


def list_backlinks(db: Session, client_id: int) -> list[Backlink]:
    stmt = (
        select(Backlink)
        .where(Backlink.client_id == client_id)
        .order_by(Backlink.authority.desc())
    )
    return list(db.scalars(stmt))


def generate_backlinks(db: Session, client_id: int, count: int = 8) -> int:
    now = datetime.now(UTC)
    for _ in range(count):
        domain = random.choice(_BACKLINK_DOMAINS)
        slug = random.randint(1000, 9999)
        db.add(
            Backlink(
                client_id=client_id,
                source_url=f"https://{domain}/post/{slug}",
                authority=random.randint(10, 95),
                discovered_at=now - timedelta(days=random.randint(0, 60)),
            )
        )
    db.commit()
    return count
