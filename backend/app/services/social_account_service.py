"""Sosyal hesap (mock) iş mantığı."""

import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.client import SocialAccount
from app.schemas.social_account import SocialAccountCreate, SocialAccountUpdate


def get_account(db: Session, account_id: int) -> SocialAccount | None:
    return db.get(SocialAccount, account_id)


def list_for_client(db: Session, client_id: int) -> list[SocialAccount]:
    stmt = select(SocialAccount).where(SocialAccount.client_id == client_id)
    return list(db.scalars(stmt))


def create_account(db: Session, client_id: int, data: SocialAccountCreate) -> SocialAccount:
    payload = data.model_dump()
    # Mock: takipçi sayısı verilmediyse gerçekçi rastgele bir değer üret.
    if not payload.get("follower_count"):
        payload["follower_count"] = random.randint(500, 250_000)
    account = SocialAccount(client_id=client_id, **payload)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account(
    db: Session, account: SocialAccount, data: SocialAccountUpdate
) -> SocialAccount:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(account, field, value)
    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, account: SocialAccount) -> None:
    db.delete(account)
    db.commit()
