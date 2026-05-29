# Modül: Analytics & Raporlama

## Amaç
Müşteri sosyal hesaplarının performansını (mock veri ile) görselleştirmek ve
sunulabilir raporlar üretmek.

## Metrikler
- Reach (erişim)
- Impressions (gösterim)
- Engagement (etkileşim: beğeni/yorum/paylaşım)
- Followers (takipçi sayısı / değişim)

## Veri Kaynağı (Faz 4)
- `AnalyticsSnapshot` kayıtları, periyodik bir Celery task'ı ile **mock**
  olarak üretilir (gerçekçi trendler simüle edilir).

## Temel Ekranlar
- Client bazlı dashboard (zaman serisi grafikleri — MUI X Charts)
- Platform karşılaştırması
- Rapor oluşturma (dönem seç → özet) ve indirme/print

## İlgili Varlıklar
`AnalyticsSnapshot`, `Report`, `Client`, `SocialAccount`

## API (taslak)
`/analytics?client_id=&from=&to=`, `/reports`
