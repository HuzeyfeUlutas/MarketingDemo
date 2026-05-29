# CLAUDE.md

Bu dosya, gelecekteki Claude (ve insan) geliştiricilere bu repoda çalışırken
rehberlik eder. Kısa ve güncel tutulmalıdır.

## Proje Özeti

Sosyal medya pazarlama ajansı için yönetim aracı (SaaS). Modüller: Müşteri &
Ekip Yönetimi, İçerik Takvimi & Planlama, Analytics & Raporlama, SEO Araçları.
Kullanıcılar: yalnızca ajans ekibi (rol tabanlı). Platform entegrasyonları
ilk fazda **mock**.

## Mimari

- **Monorepo**: `backend/` (FastAPI) + `frontend/` (React/Vite/MUI).
- Backend katmanları: `api (router)` → `services (iş mantığı + mock)` →
  `models/db`. Ayarlar `app/core/config.py` (env'den).
- Frontend: feature-bazlı (`src/features/<modul>`), ortak `components/`,
  `layouts/AppLayout.tsx`, API çağrıları `src/api/`.
- Async işler: Celery (`app/workers/celery_app.py`) + Redis.
- Migration: Alembic (`backend/alembic/`).

## Komutlar

```bash
# Tüm ortam
docker compose up --build

# Backend
cd backend && uvicorn app.main:app --reload
cd backend && pytest
cd backend && ruff check .

# Frontend
cd frontend && npm run dev
cd frontend && npm run test
cd frontend && npm run build      # tsc typecheck + vite build
```

## Konvansiyonlar

- **Secret YOK**: tüm sırlar env/`.env`'den. Detay: `SECURITY.md`.
- Python: ruff (line-length 100), tip ipuçları, Pydantic v2.
- TS: strict mode, fonksiyonel React bileşenleri.
- Yeni endpoint → `app/api/v1/endpoints/<x>.py` + `router.py`'ye kayıt.
- Yeni model → `app/models/` + `app/models/__init__.py`'den import (Alembic için)
  → `alembic revision --autogenerate` → migration.

## Branch & Git

- Aktif geliştirme branch'i: `claude/social-media-agency-tool-TLOlI`.
- Kullanıcı açıkça istemeden PR açma.

## Yol Haritası

Fazlar ve görev takibi: `docs/ROADMAP.md`. **Faz 0–5 (MVP) tamamlandı**
(iskelet, Auth & Ekip, Müşteri, İçerik, Analytics, SEO). Sırada opsiyonel
**Faz 6 (cila & gerçek entegrasyon hazırlığı)**.

## SEO (Faz 5)

- `models/seo.py`: `Keyword` + `RankTracking` + `SiteAudit` + `Backlink` (mock).
- `seo_service`: keyword + mock sıralama geçmişi, site denetimi (skor+sorunlar),
  backlink üretimi. Endpoint `seo.py` (`/seo/keywords`, `/site-audits`, `/backlinks`).
- Değişiklik yetkisi: admin/manager/seo_specialist; görüntüleme tüm ekip.
- Frontend: `features/seo/` sekmeli ekran (kelime+sıralama grafiği, denetim, backlink).

## Analytics (Faz 4)

- `models/analytics.py`: `AnalyticsSnapshot` (mock metrikler) + `Report`.
- `analytics_service`: mock üretim (trendli), tarihe göre toplulaştırma, özet,
  rapor. Endpoint `analytics.py` (`/analytics/summary`, `/generate`, `/reports`).
- Celery beat: `tasks.generate_daily_analytics` (günlük).
- Frontend: `features/analytics/` özet kartları + LineChart (@mui/x-charts).

## İçerik (Faz 3)

- `models/content.py`: `ContentItem` (durum akışı) + `Asset`. Platformlar JSON.
- Durum akışı: draft→pending_review→approved→scheduled→published (geri dönüşler
  var). Geçişler `content_service.transition` + `ALLOWED_TRANSITIONS`.
  Onay/zamanlama/yayın = admin/manager; oluştur/düzenle = +content_creator.
- Endpoint: `content.py` (`/content-items`, `.../{id}/status`, `.../assets`).
- Celery beat: `tasks.publish_scheduled_content` (60sn) zamanı geleni yayınlar.
- Frontend: `features/content/` durum panosu + içerik formu.

## Müşteri (Faz 2)

- `models/client.py`: `Client` + `SocialAccount` (mock, platform enum).
- Endpoint `clients.py`: görüntüleme tüm aktif ekip, değişiklik admin/manager
  (`require_roles(admin, manager)`). Manager atama doğrulanır.
- Frontend: `features/clients/` (liste, detay, form, sosyal hesap dialog).

## Auth (Faz 1)

- JWT access+refresh, bcrypt; `core/security.py` + `core/config.py`.
- Korumalı endpoint: `app/api/deps.py` → `CurrentUser`, `ActiveUser`,
  `require_roles(...)`. Admin'e özel işlemler `users.py`.
- İlk admin: `python -m app.db.init_db` (env: `FIRST_SUPERUSER_*`).
- Frontend: `src/auth/AuthContext.tsx` (login/logout/me), `ProtectedRoute`,
  token `src/auth/tokenStorage.ts`, 401'de otomatik refresh (`api/client.ts`).
