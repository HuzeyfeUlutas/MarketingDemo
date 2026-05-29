# Yol Haritası (Faz / Task Dökümü)

Her faz mantıksal bir teslimdir. İlerleme buradan takip edilir.

## ✅ Faz 0 — Temel İskelet & Dökümantasyon
- [x] Monorepo yapısı, `.gitignore`, `.env.example`, `docker-compose.yml`
- [x] Backend FastAPI iskeleti + `/health` endpoint
- [x] `core/config.py` (env tabanlı ayarlar)
- [x] DB session/base + Alembic kurulumu
- [x] Celery + Redis (örnek `ping` task'ı)
- [x] Frontend Vite + React + TS + MUI iskeleti, AppLayout, Dashboard
- [x] pytest (backend) + Vitest (frontend) duman testleri
- [x] GitHub Actions CI (ruff/pytest + tsc/vitest)
- [x] Dökümantasyon: README, SECURITY, CLAUDE, docs/*

## ✅ Faz 1 — Auth & Kullanıcı/Ekip Yönetimi
- [x] User modeli (rol: admin/manager/content_creator/analyst/seo_specialist) + migration
- [x] bcrypt parola hash + JWT (login/refresh/me)
- [x] Rol tabanlı yetki dependency'leri (`require_roles`)
- [x] User CRUD endpoint'leri (admin) + ilk admin seed (`init_db`)
- [x] Frontend: login sayfası, AuthContext, korumalı route'lar, token + refresh interceptor
- [x] Kullanıcı/ekip CRUD ekranları (admin)
- [x] Testler (backend: auth + users; frontend: util)

## ⏳ Faz 2 — Müşteri (Client) Yönetimi
- [ ] Client + SocialAccount modelleri (mock hesaplar)
- [ ] CRUD API + service'ler
- [ ] Frontend: müşteri listesi, detay, manager atama
- [ ] Testler

## ⏳ Faz 3 — İçerik Takvimi & Planlama
- [ ] ContentItem + Asset modelleri, durum/onay akışı
- [ ] CRUD + durum geçiş endpoint'leri
- [ ] Frontend: takvim görünümü, içerik editörü, onay
- [ ] Celery: `scheduled_at` → mock "yayınla" task'ı
- [ ] Testler

## ⏳ Faz 4 — Analytics & Raporlama
- [ ] AnalyticsSnapshot modeli + mock üreticisi (periyodik Celery)
- [ ] Metrik endpoint'leri (toplulaştırma)
- [ ] Frontend: grafikler (MUI X Charts), client dashboard'u
- [ ] Report üretimi (indirilebilir/print)
- [ ] Testler

## ⏳ Faz 5 — SEO Araçları
- [ ] Keyword/RankTracking/SiteAudit/Backlink modelleri + mock üreticiler
- [ ] Endpoint'ler
- [ ] Frontend: anahtar kelime takibi, sıralama grafiği, denetim skoru
- [ ] Testler

## ⏳ Faz 6 — Cila & Gerçek Entegrasyon Hazırlığı
- [ ] Integration adapter arayüzü (mock ↔ gerçek API)
- [ ] ActivityLog & bildirimler
- [ ] UX iyileştirmeleri, erişilebilirlik
- [ ] (Opsiyonel) gerçek Meta/Google/X entegrasyonları
