"""SEO Araçları endpoint'leri.

Görüntüleme: tüm aktif ekip. Değişiklik/üretim: admin, manager, seo_specialist.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import ActiveUser, DbSession, require_roles
from app.models.user import UserRole
from app.schemas.seo import BacklinkRead, KeywordCreate, KeywordRead, SiteAuditRead
from app.services import client_service, seo_service

router = APIRouter()

SeoUser = Annotated[
    object, Depends(require_roles(UserRole.admin, UserRole.manager, UserRole.seo_specialist))
]


def _check_client(db: DbSession, client_id: int) -> None:
    if client_service.get_client(db, client_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Müşteri bulunamadı")


# ---- Anahtar kelimeler ----


@router.get("/keywords", response_model=list[KeywordRead], summary="Anahtar kelimeleri listele")
def list_keywords(db: DbSession, _: ActiveUser, client_id: int) -> list[KeywordRead]:
    return seo_service.list_keywords(db, client_id)


@router.post(
    "/keywords",
    response_model=KeywordRead,
    status_code=status.HTTP_201_CREATED,
    summary="Anahtar kelime ekle (mock sıralama geçmişiyle)",
)
def create_keyword(db: DbSession, _: SeoUser, data: KeywordCreate) -> KeywordRead:
    _check_client(db, data.client_id)
    return seo_service.create_keyword(db, data)


@router.delete(
    "/keywords/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Anahtar kelime sil"
)
def delete_keyword(db: DbSession, _: SeoUser, keyword_id: int) -> None:
    keyword = seo_service.get_keyword(db, keyword_id)
    if keyword is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bulunamadı")
    seo_service.delete_keyword(db, keyword)


# ---- Site denetimi ----


@router.get(
    "/site-audits", response_model=list[SiteAuditRead], summary="Site denetimlerini listele"
)
def list_site_audits(db: DbSession, _: ActiveUser, client_id: int) -> list[SiteAuditRead]:
    return seo_service.list_site_audits(db, client_id)


@router.post(
    "/site-audits",
    response_model=SiteAuditRead,
    status_code=status.HTTP_201_CREATED,
    summary="Site denetimi çalıştır (mock)",
)
def run_site_audit(db: DbSession, _: SeoUser, client_id: int) -> SiteAuditRead:
    _check_client(db, client_id)
    return seo_service.run_site_audit(db, client_id)


# ---- Backlink ----


@router.get("/backlinks", response_model=list[BacklinkRead], summary="Backlink'leri listele")
def list_backlinks(db: DbSession, _: ActiveUser, client_id: int) -> list[BacklinkRead]:
    return seo_service.list_backlinks(db, client_id)


@router.post("/backlinks/generate", summary="Mock backlink üret")
def generate_backlinks(
    db: DbSession,
    _: SeoUser,
    client_id: int,
    count: Annotated[int, Query(ge=1, le=50)] = 8,
) -> dict:
    _check_client(db, client_id)
    created = seo_service.generate_backlinks(db, client_id, count)
    return {"created": created}
