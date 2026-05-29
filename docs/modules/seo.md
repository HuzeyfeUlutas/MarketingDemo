# Modül: SEO Araçları

## Amaç
Müşteri web sitelerinin arama motoru performansını (mock veri ile) takip
etmek: anahtar kelime sıralaması, site denetimi ve backlink'ler.

## Özellikler
- **Anahtar Kelime Takibi**: izlenen terimler, hedef URL, arama hacmi.
- **Sıralama (Rank) İzleme**: terim bazlı pozisyonun zaman içindeki değişimi.
- **Site Denetimi (Audit)**: genel SEO skoru + tespit edilen sorunlar (mock).
- **Backlink Takibi**: kaynak URL, otorite, keşif tarihi (mock).

## Veri Kaynağı (Faz 5)
- Mock üreticiler ile gerçekçi sıralama/skor verileri. Gelecekte gerçek SEO
  API'leri (ör. Search Console / üçüncü taraf) entegre edilebilir.

## Temel Ekranlar
- Anahtar kelime tablosu + sıralama trend grafiği
- Site denetim skor kartı + sorun listesi
- Backlink listesi

## İlgili Varlıklar
`Keyword`, `RankTracking`, `SiteAudit`, `Backlink`, `Client`

## API (taslak)
`/keywords`, `/keywords/{id}/rankings`, `/site-audits`, `/backlinks`
