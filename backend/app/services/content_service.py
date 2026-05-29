"""İçerik (ContentItem) iş mantığı: CRUD, durum geçişleri, yayınlama."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content import Asset, ContentItem, ContentStatus
from app.models.user import User
from app.schemas.content import AssetCreate, ContentItemCreate, ContentItemUpdate

# İzin verilen durum geçişleri.
ALLOWED_TRANSITIONS: dict[ContentStatus, set[ContentStatus]] = {
    ContentStatus.draft: {ContentStatus.pending_review},
    ContentStatus.pending_review: {ContentStatus.approved, ContentStatus.draft},
    ContentStatus.approved: {ContentStatus.scheduled, ContentStatus.draft},
    ContentStatus.scheduled: {ContentStatus.published, ContentStatus.approved},
    ContentStatus.published: set(),
}

# Onay/yayın yetkisi gerektiren hedef durumlar (admin/manager).
APPROVAL_TARGETS = {ContentStatus.approved, ContentStatus.scheduled, ContentStatus.published}


class TransitionError(ValueError):
    """Geçersiz durum geçişi."""


def get_content(db: Session, content_id: int) -> ContentItem | None:
    return db.get(ContentItem, content_id)


def list_content(
    db: Session,
    client_id: int | None = None,
    status: ContentStatus | None = None,
    skip: int = 0,
    limit: int = 200,
) -> list[ContentItem]:
    stmt = select(ContentItem)
    if client_id is not None:
        stmt = stmt.where(ContentItem.client_id == client_id)
    if status is not None:
        stmt = stmt.where(ContentItem.status == status)
    stmt = stmt.order_by(ContentItem.scheduled_at.is_(None), ContentItem.scheduled_at)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt))


def create_content(db: Session, data: ContentItemCreate, created_by: User) -> ContentItem:
    item = ContentItem(
        client_id=data.client_id,
        title=data.title,
        body=data.body,
        platforms=list(data.platforms),
        scheduled_at=data.scheduled_at,
        created_by_id=created_by.id,
        status=ContentStatus.draft,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_content(db: Session, item: ContentItem, data: ContentItemUpdate) -> ContentItem:
    update_data = data.model_dump(exclude_unset=True)
    if "platforms" in update_data and update_data["platforms"] is not None:
        update_data["platforms"] = list(update_data["platforms"])
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_content(db: Session, item: ContentItem) -> None:
    db.delete(item)
    db.commit()


def transition(
    db: Session,
    item: ContentItem,
    target: ContentStatus,
    actor: User,
    scheduled_at: datetime | None = None,
) -> ContentItem:
    """İçeriğin durumunu değiştirir; geçiş kurallarını uygular."""
    if target not in ALLOWED_TRANSITIONS[item.status]:
        raise TransitionError(f"{item.status} → {target} geçişi geçersiz")

    if target == ContentStatus.scheduled:
        new_time = scheduled_at or item.scheduled_at
        if new_time is None:
            raise TransitionError("Zamanlama için scheduled_at gereklidir")
        item.scheduled_at = new_time

    if target == ContentStatus.approved:
        item.approved_by_id = actor.id

    if target == ContentStatus.published:
        item.published_at = datetime.now(UTC)

    if target == ContentStatus.draft:
        # Taslağa geri dönüşte onay bilgisini temizle.
        item.approved_by_id = None

    item.status = target
    db.commit()
    db.refresh(item)
    return item


def add_asset(db: Session, item: ContentItem, data: AssetCreate) -> Asset:
    asset = Asset(content_item_id=item.id, **data.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset: Asset) -> None:
    db.delete(asset)
    db.commit()


def publish_due_scheduled(db: Session) -> int:
    """Zamanı gelmiş (scheduled_at <= now) zamanlanmış içerikleri yayınlar.

    Celery task'ı tarafından periyodik çağrılır. Yayınlanan içerik sayısını döner.
    """
    now = datetime.now(UTC)
    stmt = select(ContentItem).where(
        ContentItem.status == ContentStatus.scheduled,
        ContentItem.scheduled_at.is_not(None),
        ContentItem.scheduled_at <= now,
    )
    due = list(db.scalars(stmt))
    for item in due:
        item.status = ContentStatus.published
        item.published_at = now
    if due:
        db.commit()
    return len(due)
