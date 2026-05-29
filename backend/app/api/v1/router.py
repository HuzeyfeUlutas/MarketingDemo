"""API v1 ana router'ı.

Sonraki fazlarda eklenecek alt router'lar (seo) burada birleştirilecek.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analytics, auth, clients, content, health, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(content.router, prefix="/content-items", tags=["content"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
