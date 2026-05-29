"""İçerik (ContentItem) yönetimi endpoint'leri.

Görüntüleme: tüm aktif ekip.
Oluştur/düzenle/sil (taslak): content_creator, manager, admin.
Onay/zamanlama/yayın geçişleri: manager, admin.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import ActiveUser, DbSession, require_roles
from app.models.content import ContentStatus
from app.models.user import UserRole
from app.schemas.content import (
    AssetCreate,
    AssetRead,
    ContentItemCreate,
    ContentItemRead,
    ContentItemUpdate,
    ContentStatusUpdate,
)
from app.services import client_service, content_service
from app.services.content_service import APPROVAL_TARGETS, TransitionError

router = APIRouter()

# İçerik oluşturma/düzenleme yetkisi.
EditorUser = Annotated[
    object, Depends(require_roles(UserRole.admin, UserRole.manager, UserRole.content_creator))
]
ApproverUser = Annotated[object, Depends(require_roles(UserRole.admin, UserRole.manager))]


def _get_or_404(db: DbSession, content_id: int):
    item = content_service.get_content(db, content_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İçerik bulunamadı")
    return item


@router.get("", response_model=list[ContentItemRead], summary="İçerikleri listele")
def list_content(
    db: DbSession,
    _: ActiveUser,
    client_id: int | None = None,
    status: ContentStatus | None = None,
) -> list[ContentItemRead]:
    return content_service.list_content(db, client_id=client_id, status=status)


@router.post(
    "",
    response_model=ContentItemRead,
    status_code=status.HTTP_201_CREATED,
    summary="İçerik oluştur",
)
def create_content(
    db: DbSession, current_user: ActiveUser, data: ContentItemCreate, _: EditorUser
) -> ContentItemRead:
    if client_service.get_client(db, data.client_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Geçersiz müşteri")
    return content_service.create_content(db, data, created_by=current_user)


@router.get("/{content_id}", response_model=ContentItemRead, summary="Tek içerik")
def get_content(db: DbSession, _: ActiveUser, content_id: int) -> ContentItemRead:
    return _get_or_404(db, content_id)


@router.patch("/{content_id}", response_model=ContentItemRead, summary="İçerik güncelle")
def update_content(
    db: DbSession, _: EditorUser, content_id: int, data: ContentItemUpdate
) -> ContentItemRead:
    item = _get_or_404(db, content_id)
    if item.status == ContentStatus.published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Yayınlanmış içerik düzenlenemez"
        )
    return content_service.update_content(db, item, data)


@router.delete(
    "/{content_id}", status_code=status.HTTP_204_NO_CONTENT, summary="İçerik sil"
)
def delete_content(db: DbSession, _: EditorUser, content_id: int) -> None:
    item = _get_or_404(db, content_id)
    content_service.delete_content(db, item)


@router.post(
    "/{content_id}/status",
    response_model=ContentItemRead,
    summary="İçerik durumunu değiştir (onay akışı)",
)
def change_status(
    db: DbSession, current_user: ActiveUser, content_id: int, data: ContentStatusUpdate
) -> ContentItemRead:
    item = _get_or_404(db, content_id)

    # Onay/zamanlama/yayın geçişleri yalnızca admin/manager.
    if data.status in APPROVAL_TARGETS and current_user.role not in (
        UserRole.admin,
        UserRole.manager,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Bu geçiş için yetkiniz yok"
        )
    # Taslak/incelemeye gönderme: editör rolleri.
    if current_user.role not in (
        UserRole.admin,
        UserRole.manager,
        UserRole.content_creator,
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yetkiniz yok")

    try:
        return content_service.transition(
            db, item, data.status, actor=current_user, scheduled_at=data.scheduled_at
        )
    except TransitionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


# ---- Medya (Asset) ----


@router.post(
    "/{content_id}/assets",
    response_model=AssetRead,
    status_code=status.HTTP_201_CREATED,
    summary="İçeriğe medya ekle",
)
def add_asset(
    db: DbSession, _: EditorUser, content_id: int, data: AssetCreate
) -> AssetRead:
    item = _get_or_404(db, content_id)
    return content_service.add_asset(db, item, data)


@router.delete(
    "/{content_id}/assets/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Medya sil",
)
def delete_asset(db: DbSession, _: EditorUser, content_id: int, asset_id: int) -> None:
    item = _get_or_404(db, content_id)
    asset = next((a for a in item.assets if a.id == asset_id), None)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medya bulunamadı")
    content_service.delete_asset(db, asset)
