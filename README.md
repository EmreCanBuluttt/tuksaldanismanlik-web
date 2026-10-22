# tuksaldanismanlik.com — TUKSAL Danışmanlık kurumsal sitesi

Müşteri: **TUKSAL Danışmanlık / Emel Özbek Eğitim ve Proje Ajansı**. Statik site, framework ve sunucu yok.
Yayın: **GitHub Pages** (`main` dalı, `docs/` klasörü) → **https://www.tuksaldanismanlik.com**.
Her `git push` 1-2 dakikada yayına çıkar.

## Klasörler

| Yol | Ne |
|---|---|
| `docs/` | **Yayınlanan site.** HTML'ler `build.py` ile üretilir; `assets/` (CSS, JS, font, görsel, veri) burada elle düzenlenir. `CNAME` ve `.nojekyll` silinmez. |
| `content/<slug>.html` | Her sayfanın `<main>` içi. Metin değişikliği burada yapılır. |
| `content/pages.json` | Site bilgileri, menü, footer, sayfa başlık/açıklamaları. `"hidden": true` olan sayfa üretilmez, menüden ve site haritasından düşer. |
| `templates/page.html` | Ortak iskelet (head, menü, footer). |
| `build.py` | `content/` + şablon → `docs/*.html`, `sitemap.xml`, `robots.txt`. `--check` kırık bağlantı/anchor/alt/h1 denetler. |
| `DESIGN.md` | Tasarım sistemi ve yazım kuralları. |
| `tools/` | Görsel üretim/işleme betikleri (şu an kullanılmıyor, bkz. Görsel ilkesi). |
| `_arsiv/yapim-asamasi/` | 18-22 Eki 2026'da yayında olan "yapım aşamasında" sayfası (geri dönmek için). |
| `kaynak/`, `_gorsel-arsiv/` | Müşteri briefi ve eski yapay zekâ fotoğrafları. **Depoya girmez** (`.gitignore`), yalnız yerelde. |

## Güncelleme

```bash
python3 build.py --check          # content/ değiştiyse
git add -A && git commit -m "..." && git push
```

Build gerektirmeyen dosyalar (doğrudan düzenle + push):

- `docs/assets/js/config.js` — e-posta, telefon, WhatsApp, form adresi. **Boş bırakılan her kanal sitede gizlenir.**
  Hepsi boşken İletişim sayfası "çok yakında" notu gösterir ve form gizlenir. Form, `formEndpoint`
  (ör. Formspree) ya da `email` dolunca görünür.
- `docs/assets/data/etkinlikler.js` — etkinlik takvimi (dosyada örnek kayıt şablonu var). Boşken
  "Yaklaşan etkinlik bulunmuyor" yazar.

## Görsel ilkesi

Sitede **insan fotoğrafı yok.** Yapay zekâyla üretilmiş kişiler kurucu ya da ekip sanılabildiği için
kaldırıldı (müşteri kararı, 18 Eki 2026). Başlıklarda lacivert zemin + logo işareti, kart ve panellerde
hizmete özel ikon kutuları kullanılıyor. Gerçek fotoğraf gerekiyorsa yalnız müşterinin kendi fotoğrafları.
Emel Özbek fotoğrafı gelince `content/hakkimizda.html` içindeki `.founder-placeholder` bloğu değiştirilir.

## Alan adı, DNS, HTTPS

GoDaddy DNS: `A @` → 185.199.108.153 / .109 / .110 / .111 ve `CNAME www` → `emrecanbuluttt.github.io`.
Kök adres www'ye yönlenir. HTTPS zorunlu (Let's Encrypt, GitHub kendisi yeniler).
Sertifika DNS doğru olduğu hâlde gelmezse: Settings → Pages'te özel alan adını kaldırıp yeniden ekle
(API: `cname` önce `null`, sonra `www.tuksaldanismanlik.com`).

## Açık konular

- **İletişim kanalı:** e-posta, telefon ve form henüz tanımlı değil. Gelince `docs/assets/js/config.js`'e yaz;
  iletişim sayfası, footer ve sayfa sonu çağrıları kendiliğinden açılır.
- **Referanslar** sayfası gizli (`pages.json` → `hidden`). Taranmış mektuplar gelince `content/referanslar.html`
  içindeki talimata göre ekle ve `hidden`'ı kaldır.
- **Mathvivor** kartı şimdilik bağlantısız; bağlantı eklemek için `content/anlasmali-markalar.html`'deki nota bak.
- **KVKK metni** yayına almadan önce müşteriyle birlikte gözden geçirilmeli.

## Yapım aşaması moduna dönmek

`_arsiv/yapim-asamasi/docs/` içeriğini `docs/` yerine koy (`CNAME` korunarak) ve push et.
