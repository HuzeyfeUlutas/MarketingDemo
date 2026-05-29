"""Müşteri (Client) iş mantığı (CRUD)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.user import User, UserRole
from app.schemas.client import ClientCreate, ClientUpdate


def get_client(db: Session, client_id: int) -> Client | None:
    return db.get(Client, client_id)


def list_clients(db: Session, skip: int = 0, limit: int = 100) -> list[Client]:
    stmt = select(Client).order_by(Client.name).offset(skip).limit(limit)
    return list(db.scalars(stmt))


def list_assignable_managers(db: Session) -> list[User]:
    """Müşteriye atanabilecek kullanıcılar: admin ve manager rolleri (aktif)."""
    stmt = select(User).where(
        User.is_active.is_(True),
        User.role.in_([UserRole.admin, UserRole.manager]),
    )
    return list(db.scalars(stmt))


def manager_exists(db: Session, manager_id: int) -> bool:
    user = db.get(User, manager_id)
    return user is not None and user.role in (UserRole.admin, UserRole.manager)


def create_client(db: Session, data: ClientCreate) -> Client:
    client = Client(**data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db: Session, client: Client, data: ClientUpdate) -> Client:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client: Client) -> None:
    db.delete(client)
    db.commit()
