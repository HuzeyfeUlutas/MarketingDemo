"""API v1 ana router'ı.

Sonraki fazlarda eklenecek alt router'lar (content, analytics, seo)
burada birleştirilecek.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, clients, health, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
