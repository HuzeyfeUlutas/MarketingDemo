# Proje Genel Bakış

## Vizyon

Sosyal medya pazarlama ajanslarının dağınık araçlar (tablo, takvim, ayrı
analytics panelleri, SEO araçları) yerine **tek bir merkezi platformdan**
tüm müşteri operasyonlarını yönetmesini sağlamak.

## Hedef Kitle

Bir dijital pazarlama / sosyal medya ajansının **çalışanları**:
- **Admin** — sistem ve ekip yönetimi
- **Account Manager** — müşteri ilişkileri, onay
- **Content Creator** — içerik üretimi ve planlama
- **Analyst** — performans analizi ve raporlama
- **SEO Specialist** — SEO takibi ve denetimi

> İlk sürümde **müşteri (client) girişi yoktur**; sistemi yalnızca ajans
> ekibi kullanır. Müşteriler veri/raporlarda bir varlık (entity) olarak
> temsil edilir.

## Çözülen Problem

- Müşteri başına dağınık içerik takvimleri ve onay süreçleri
- Manuel, tekrar eden raporlama
- Sosyal performans + SEO verisinin tek yerde olmaması

## MVP Kapsamı

1. **Müşteri & Ekip Yönetimi** — müşteri şirketleri, sosyal hesaplar, ekip,
   roller.
2. **İçerik Takvimi & Planlama** — gönderi taslakları, onay akışı,
   zamanlama.
3. **Analytics & Raporlama** — metrik panoları ve raporlar (mock veri).
4. **SEO Araçları** — anahtar kelime/sıralama takibi, site denetimi (mock).

## Alınan Kararlar

| Konu | Karar | Gerekçe |
|------|-------|---------|
| Backend | FastAPI | Async, hızlı, otomatik OpenAPI, React ile uyum |
| DB | PostgreSQL | İlişkisel, olgun, güvenilir |
| Frontend | React + Vite + MUI | Hızlı geliştirme, hazır kurumsal bileşenler |
| Async | Celery + Redis | Zamanlanmış yayın, rapor/SEO arka plan işleri |
| Ortam | Docker Compose | Tutarlı, tek komutla kurulum |
| Test | pytest + Vitest | Standart, güçlü ekosistem |
| CI | GitHub Actions | Repo ile entegre |
| Entegrasyon | Önce mock | API onay/key süreçlerine takılmadan ilerlemek |
| Kullanıcı | Sadece ajans ekibi | MVP'yi sade tutmak |

## Kapsam Dışı (Şimdilik)

- Gerçek platform API entegrasyonları (sonraki faz)
- Müşteri self-servis portalı
- Çok-ajanslı (multi-tenant) mimari
- Faturalandırma/billing
