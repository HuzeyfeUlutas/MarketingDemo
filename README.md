# Social Media Agency Tool

Bir sosyal medya pazarlama ajansının operasyonlarını tek panelden yönetmesi
için geliştirilen web uygulaması. Ajans; **müşterilerini**, **içerik
takvimini & onay akışını**, **performans analitiğini/raporlamasını** ve **SEO
çalışmalarını** buradan yönetir.

> İlk fazda platform entegrasyonları (Meta, Google, X...) **mock/simülasyon**
> verisiyle çalışır. Gerçek API entegrasyonu sonraki faza bırakılmıştır.

## Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Veritabanı | PostgreSQL |
| Arka plan | Celery + Redis |
| Frontend | React + TypeScript + Vite + Material UI (MUI) |
| Test | pytest (backend), Vitest (frontend) |
| CI | GitHub Actions |
| Ortam | Docker Compose |

## Hızlı Başlangıç (Docker)

```bash
# 1) Ortam değişkenlerini hazırlayın (gerçek secret'ları .env'e yazın)
cp .env.example .env

# 2) Tüm servisleri ayağa kaldırın
docker compose up --build
```

Servisler:
- Backend API → http://localhost:8000  (Swagger: http://localhost:8000/docs)
- Frontend → http://localhost:5173
- PostgreSQL → localhost:5432, Redis → localhost:6379

## Lokal Geliştirme (Docker'sız)

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"          # test/lint araçları
uvicorn app.main:app --reload
pytest                            # testler
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
npm run test
```

## Proje Yapısı ve Dökümantasyon

Temel yapılar `docs/` altında saklanır:

- [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) — vizyon ve kararlar
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — sistem mimarisi
- [docs/DATA_MODEL.md](docs/DATA_MODEL.md) — veri modeli (ER diyagramı)
- [docs/API.md](docs/API.md) — API konvansiyonları
- [docs/ROADMAP.md](docs/ROADMAP.md) — faz/task yol haritası
- [docs/modules/](docs/modules/) — modül spec'leri
- [SECURITY.md](SECURITY.md) — **güvenlik ve secret yönetimi**
- [CLAUDE.md](CLAUDE.md) — geliştirme rehberi (komutlar/konvansiyonlar)

## Güvenlik

Repoda **hiçbir secret bulunmaz**. Tüm sırlar `.env` (gitignore'lu) veya
ortam değişkenlerinden okunur. Detaylar: [SECURITY.md](SECURITY.md).
