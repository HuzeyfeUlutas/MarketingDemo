"""Uygulama ayarları.

TÜM yapılandırma (özellikle secret'lar) ortam değişkenlerinden / .env'den
okunur. Repoda hiçbir secret hard-code edilmez (bkz. SECURITY.md).
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Genel
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Social Media Agency Tool"
    API_V1_PREFIX: str = "/api/v1"

    # CORS — frontend origin'leri
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # Veritabanı
    DATABASE_URL: str = "postgresql+psycopg://agency:change_me_in_local_env@db:5432/agency"

    # Redis / Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # Auth / JWT  (üretimde JWT_SECRET_KEY mutlaka env'den verilmelidir)
    JWT_SECRET_KEY: str = "dev-only-insecure-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
