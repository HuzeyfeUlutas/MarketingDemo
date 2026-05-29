"""API v1 ana router'ı.

Sonraki fazlarda eklenecek alt router'lar (auth, users, clients, content,
analytics, seo) burada birleştirilecek.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])

# Faz 1+ örnek:
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
