"""Kimlik doğrulama endpoint'leri: login, refresh, me."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from app.api.deps import ActiveUser, DbSession
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import AccessToken, RefreshRequest, Token
from app.schemas.user import UserRead
from app.services import user_service

router = APIRouter()


@router.post("/login", response_model=Token, summary="E-posta + parola ile giriş")
def login(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # OAuth2 form'unda kullanıcı adı alanı e-posta olarak kullanılır.
    user = user_service.authenticate(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta veya parola hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Pasif kullanıcı")
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=AccessToken, summary="Refresh token ile yeni access token")
def refresh(db: DbSession, body: RefreshRequest) -> AccessToken:
    try:
        payload = decode_token(body.refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz refresh token"
        ) from exc

    user = user_service.get_user(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Geçersiz kullanıcı")
    return AccessToken(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserRead, summary="Mevcut kullanıcı bilgisi")
def me(current_user: ActiveUser) -> UserRead:
    return current_user
