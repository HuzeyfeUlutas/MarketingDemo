# API Konvansiyonları

## Temel İlkeler

- **REST**, JSON gövde. Base path: `/api/v1`.
- Interaktif dokümantasyon: `GET /docs` (Swagger), `GET /redoc`.
- OpenAPI şeması: `/api/v1/openapi.json`.

## Versiyonlama

- URL bazlı: `/api/v1/...`. Kıran (breaking) değişiklikler `/api/v2` ile.

## Kaynak (Resource) Adlandırma

- Çoğul, kebab/lowercase: `/clients`, `/content-items`, `/keywords`.
- Standart CRUD:
  - `GET /clients` — liste (sayfalama: `?page=&size=`)
  - `POST /clients` — oluştur
  - `GET /clients/{id}` — tekil
  - `PATCH /clients/{id}` — kısmi güncelle
  - `DELETE /clients/{id}` — sil

## Kimlik Doğrulama

- `POST /api/v1/auth/login` → access + refresh token (JWT).
- Korumalı endpoint'ler: `Authorization: Bearer <access_token>`.
- `POST /api/v1/auth/refresh` → yeni access token.

## Hata Formatı

FastAPI varsayılanı kullanılır:

```json
{ "detail": "Açıklayıcı hata mesajı" }
```

Doğrulama hataları (422) alan bazlı `detail` listesi döner. HTTP durum
kodları semantik kullanılır (400, 401, 403, 404, 409, 422, 500).

## Sayfalama / Filtre / Sıralama

- Sayfalama: `?page=1&size=20`.
- Filtre: kaynağa özel query parametreleri (örn. `?status=published`).
- Sıralama: `?sort=-created_at` (`-` azalan).

## Health

- `GET /health` ve `GET /api/v1/health` → `{ "status": "ok", ... }`.
