# Modül: Müşteri & Ekip Yönetimi

## Amaç
Ajansın yönettiği müşteri şirketleri, onların sosyal hesaplarını ve ajans
ekibini (kullanıcı + rol) yönetmek. Diğer tüm modüllerin temelidir.

## Kapsam
- **Ekip**: kullanıcı oluşturma, rol atama, aktif/pasif etme.
- **Müşteri (Client)**: şirket bilgisi, sektör, sorumlu manager, durum.
- **Sosyal Hesap**: client'a bağlı mock hesaplar (platform, handle, follower).

## Roller
| Rol | Yetki (özet) |
|-----|--------------|
| admin | her şey + kullanıcı yönetimi |
| manager | müşteri yönetimi, içerik onayı |
| content_creator | içerik oluşturma/düzenleme |
| analyst | analytics/rapor görüntüleme |
| seo_specialist | SEO modülü |

## Temel Ekranlar
- Müşteri listesi + detay
- Ekip/kullanıcı yönetimi (admin)
- Sosyal hesap ekleme (mock)

## İlgili Varlıklar
`User`, `Client`, `SocialAccount` (bkz. docs/DATA_MODEL.md)

## API (taslak)
`/auth`, `/users`, `/clients`, `/clients/{id}/social-accounts`
