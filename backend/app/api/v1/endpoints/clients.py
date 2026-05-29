"""Müşteri (Client) ve sosyal hesap yönetimi endpoint'leri.

Görüntüleme: tüm aktif ekip üyeleri.
Değiştirme (oluştur/güncelle/sil): admin veya manager.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import ActiveUser, DbSession, require_roles
from app.models.user import UserRole
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.schemas.social_account import (
    SocialAccountCreate,
    SocialAccountRead,
    SocialAccountUpdate,
)
from app.schemas.user import UserSummary
from app.services import client_service, social_account_service

router = APIRouter()

# Müşteri/sosyal hesap değişiklikleri admin veya manager gerektirir.
ManagerUser = Annotated[object, Depends(require_roles(UserRole.admin, UserRole.manager))]


def _get_client_or_404(db: DbSession, client_id: int):
    client = client_service.get_client(db, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Müşteri bulunamadı")
    return client


@router.get("", response_model=list[ClientRead], summary="Müşterileri listele")
def list_clients(
    db: DbSession, _: ActiveUser, skip: int = 0, limit: int = 100
) -> list[ClientRead]:
    return client_service.list_clients(db, skip=skip, limit=limit)


@router.get(
    "/assignable-managers",
    response_model=list[UserSummary],
    summary="Müşteriye atanabilecek yöneticiler (admin/manager)",
)
def assignable_managers(db: DbSession, _: ManagerUser) -> list[UserSummary]:
    return client_service.list_assignable_managers(db)


@router.post(
    "", response_model=ClientRead, status_code=status.HTTP_201_CREATED, summary="Müşteri oluştur"
)
def create_client(db: DbSession, _: ManagerUser, data: ClientCreate) -> ClientRead:
    if data.manager_id is not None and not client_service.manager_exists(db, data.manager_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Geçersiz yönetici (manager)"
        )
    return client_service.create_client(db, data)


@router.get("/{client_id}", response_model=ClientRead, summary="Tek müşteri")
def get_client(db: DbSession, _: ActiveUser, client_id: int) -> ClientRead:
    return _get_client_or_404(db, client_id)


@router.patch("/{client_id}", response_model=ClientRead, summary="Müşteri güncelle")
def update_client(
    db: DbSession, _: ManagerUser, client_id: int, data: ClientUpdate
) -> ClientRead:
    client = _get_client_or_404(db, client_id)
    if data.manager_id is not None and not client_service.manager_exists(db, data.manager_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Geçersiz yönetici (manager)"
        )
    return client_service.update_client(db, client, data)


@router.delete(
    "/{client_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Müşteri sil"
)
def delete_client(db: DbSession, _: ManagerUser, client_id: int) -> None:
    client = _get_client_or_404(db, client_id)
    client_service.delete_client(db, client)


# ---- Sosyal hesaplar (mock) ----


@router.post(
    "/{client_id}/social-accounts",
    response_model=SocialAccountRead,
    status_code=status.HTTP_201_CREATED,
    summary="Müşteriye sosyal hesap ekle (mock)",
)
def add_social_account(
    db: DbSession, _: ManagerUser, client_id: int, data: SocialAccountCreate
) -> SocialAccountRead:
    _get_client_or_404(db, client_id)
    return social_account_service.create_account(db, client_id, data)


@router.patch(
    "/{client_id}/social-accounts/{account_id}",
    response_model=SocialAccountRead,
    summary="Sosyal hesabı güncelle",
)
def update_social_account(
    db: DbSession,
    _: ManagerUser,
    client_id: int,
    account_id: int,
    data: SocialAccountUpdate,
) -> SocialAccountRead:
    account = social_account_service.get_account(db, account_id)
    if account is None or account.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hesap bulunamadı")
    return social_account_service.update_account(db, account, data)


@router.delete(
    "/{client_id}/social-accounts/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sosyal hesabı sil",
)
def delete_social_account(
    db: DbSession, _: ManagerUser, client_id: int, account_id: int
) -> None:
    account = social_account_service.get_account(db, account_id)
    if account is None or account.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hesap bulunamadı")
    social_account_service.delete_account(db, account)
