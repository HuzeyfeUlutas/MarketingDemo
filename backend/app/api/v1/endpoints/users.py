"""Kullanıcı/ekip yönetimi endpoint'leri (yalnızca admin)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import ActiveUser, DbSession, require_roles
from app.models.user import UserRole
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter()

# Tüm ekip yönetimi işlemleri admin yetkisi gerektirir.
AdminUser = Annotated[object, Depends(require_roles(UserRole.admin))]


@router.get("", response_model=list[UserRead], summary="Kullanıcıları listele")
def list_users(db: DbSession, _: AdminUser, skip: int = 0, limit: int = 100) -> list[UserRead]:
    return user_service.list_users(db, skip=skip, limit=limit)


@router.post(
    "", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Kullanıcı oluştur"
)
def create_user(db: DbSession, _: AdminUser, data: UserCreate) -> UserRead:
    if user_service.get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Bu e-posta zaten kayıtlı"
        )
    return user_service.create_user(db, data)


@router.get("/{user_id}", response_model=UserRead, summary="Tek kullanıcı")
def get_user(db: DbSession, _: AdminUser, user_id: int) -> UserRead:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")
    return user


@router.patch("/{user_id}", response_model=UserRead, summary="Kullanıcı güncelle")
def update_user(db: DbSession, _: AdminUser, user_id: int, data: UserUpdate) -> UserRead:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")
    return user_service.update_user(db, user, data)


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Kullanıcı sil"
)
def delete_user(db: DbSession, current_user: ActiveUser, user_id: int) -> None:
    # Yetki kontrolü: yalnızca admin (current_user.role) ve kendini silememe.
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yetkiniz yok")
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Kendinizi silemezsiniz"
        )
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanıcı bulunamadı")
    user_service.delete_user(db, user)
