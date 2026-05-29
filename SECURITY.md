# Güvenlik Politikası

Bu doküman, projenin güvenlik ve **secret yönetimi** kurallarını tanımlar.
Tüm katkıda bulunanlar bu kurallara uymak zorundadır.

## 1. Temel Kural: Repoda Secret Bulunmaz

**Hiçbir API key, parola, token, private key veya bağlantı secret'ı repoya
commit edilmez.** Bu kapsamda olanlar:

- Veritabanı parolaları (`POSTGRES_PASSWORD`, `DATABASE_URL`)
- JWT imzalama anahtarı (`JWT_SECRET_KEY`)
- Üçüncü taraf platform anahtarları (Meta, Google Ads, X, vb. — gelecek faz)
- Servis hesabı JSON'ları, `.pem`/`.key` dosyaları

### Nasıl saklanır?

| Ortam | Yöntem |
|-------|--------|
| Lokal geliştirme | `.env` dosyası (git tarafından **yok sayılır**) |
| CI (GitHub Actions) | GitHub **Actions Secrets** |
| Üretim/Staging | Platform secret store / ortam değişkenleri |

Repoya yalnızca **`.env.example`** girer — bu dosya **gerçek değer içermez**,
sadece anahtar isimlerini ve açıklamalarını barındırır.

## 2. Yapılandırma Akışı

- Backend tüm ayarları `app/core/config.py` içindeki Pydantic `Settings`
  sınıfı ile **ortam değişkenlerinden** okur. Kod içinde secret hard-code
  edilmez.
- Frontend yalnızca **secret olmayan** `VITE_*` değişkenlerini kullanır
  (ör. API base URL). Vite, `VITE_` öneki olan değişkenleri istemciye
  gömer; bu yüzden oraya **asla** gizli değer konmaz.
- Alembic, DB URL'ini `alembic.ini` yerine `app.core.config.settings`
  üzerinden alır.

## 3. `.gitignore` Koruması

Aşağıdakiler git tarafından yok sayılır: `.env`, `.env.*` (`.env.example`
hariç), `*.pem`, `*.key`, `*.p12`, `credentials*.json`,
`service-account*.json`, `secrets/`.

## 4. Kimlik Doğrulama (Auth)

- Parolalar **bcrypt** ile hash'lenerek saklanır (asla düz metin).
- Oturum yönetimi **JWT** (access + refresh) ile yapılır; `JWT_SECRET_KEY`
  yalnızca env'den gelir.
- Üretimde güçlü bir anahtar üretin: `openssl rand -hex 32`.
- Rol tabanlı yetkilendirme (admin / manager / content_creator / analyst /
  seo_specialist) endpoint seviyesinde uygulanır.

## 5. Bağımlılık & Tarama Önerileri

- Commit öncesi secret taraması: [`gitleaks`](https://github.com/gitleaks/gitleaks).
- CI'da bağımlılık denetimi (örn. `pip-audit`, `npm audit`).
- GitHub **secret scanning** ve **Dependabot** etkinleştirilmesi önerilir.

## 6. Yanlışlıkla Commit Edilen Secret

Bir secret yanlışlıkla commit edilirse:
1. İlgili anahtarı **derhal iptal edip yenileyin** (rotate).
2. Geçmişten temizleyin (`git filter-repo` / BFG) ve force-push edin.
3. Olayı ekiple paylaşın.

> Not: Bir secret bir kez push edildiyse, geçmişten silinse bile **sızmış**
> kabul edilmeli ve mutlaka rotate edilmelidir.

## 7. Sorumlu İfşa (Responsible Disclosure)

Güvenlik açığı tespit ederseniz, herkese açık issue açmak yerine proje
sorumlusuyla özel olarak iletişime geçin.
