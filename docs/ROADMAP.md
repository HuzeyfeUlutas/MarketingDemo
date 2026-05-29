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

## ✅ Faz 2 — Müşteri (Client) Yönetimi
- [x] Client + SocialAccount modelleri (mock hesaplar) + migration
- [x] CRUD API + service'ler (görüntüleme: tüm ekip; değişiklik: admin/manager)
- [x] Manager atama + doğrulama, atanabilir yönetici listesi endpoint'i
- [x] Frontend: müşteri listesi, detay (sosyal hesap ekle/sil), form/manager atama
- [x] Testler (backend: client + sosyal hesap akışı; frontend: util)

## ✅ Faz 3 — İçerik Takvimi & Planlama
- [x] ContentItem + Asset modelleri, durum/onay akışı + migration 0003
- [x] CRUD + durum geçiş endpoint'i (`/content-items/{id}/status`) ve geçiş kuralları
- [x] Frontend: durum panosu (planlama board), içerik editörü dialog, onay aksiyonları
- [x] Celery: beat ile `publish_scheduled_content` (scheduled_at gelince mock yayın)
- [x] Testler (backend: akış + yayınlama; frontend: util)

## ✅ Faz 4 — Analytics & Raporlama
- [x] AnalyticsSnapshot + Report modelleri + migration 0004
- [x] Mock metrik üreticisi + periyodik Celery task (`generate_daily_analytics`)
- [x] Metrik endpoint'leri: `/analytics/summary` (toplulaştırma + zaman serisi), `/generate`
- [x] Frontend: özet kartları + çizgi grafik (MUI X Charts), müşteri/dönem seçimi
- [x] Rapor üretimi + listeleme (`/analytics/reports`)
- [x] Testler (backend: üretim/özet/rapor; frontend: util)

## ✅ Faz 5 — SEO Araçları  →  🎉 MVP TAMAMLANDI
- [x] Keyword/RankTracking/SiteAudit/Backlink modelleri + mock üreticiler + migration 0005
- [x] Endpoint'ler (`/seo/keywords`, `/site-audits`, `/backlinks`)
- [x] Frontend: anahtar kelime takibi + sıralama trend grafiği, site denetim skoru, backlink listesi
- [x] Testler (backend: keyword/rank, audit, backlink, yetki)

## ⏳ Faz 6 — Cila & Gerçek Entegrasyon Hazırlığı
- [ ] Integration adapter arayüzü (mock ↔ gerçek API)
- [ ] ActivityLog & bildirimler
- [ ] UX iyileştirmeleri, erişilebilirlik
- [ ] (Opsiyonel) gerçek Meta/Google/X entegrasyonları
