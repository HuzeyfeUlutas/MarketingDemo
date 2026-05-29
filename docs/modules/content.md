# Modül: İçerik Takvimi & Planlama

## Amaç
Müşteriler için sosyal medya içeriklerini planlamak, dahili onay sürecinden
geçirmek ve zamanlanmış (mock) yayınlamak.

## İçerik Durum Akışı
```
draft → pending_review → approved → scheduled → published
                     ↘ (geri) draft
```
- **draft**: content_creator oluşturur/düzenler.
- **pending_review**: onay bekler.
- **approved**: manager onaylar.
- **scheduled**: `scheduled_at` belirlenir.
- **published**: Celery task'ı zamanı gelince mock yayınlar.

## Temel Ekranlar
- Aylık/haftalık takvim görünümü
- İçerik editörü (metin, platform seçimi, medya/asset)
- Onay paneli (manager)

## Arka Plan İşleri
- Celery: `scheduled_at` gelen içerikleri `published` yapar (mock).

## İlgili Varlıklar
`ContentItem`, `Asset`, `Client`, `User` (bkz. docs/DATA_MODEL.md)

## API (taslak)
`/content-items`, `/content-items/{id}/status`, `/assets`
