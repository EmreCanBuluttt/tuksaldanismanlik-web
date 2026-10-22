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

- `docs/assets/js/config.js` — adres, telefonlar, e-posta, WhatsApp, form adresi. **Boş bırakılan her kanal sitede gizlenir.**
  Form, `formEndpoint` ya da `email` dolunca görünür; `formEndpoint` boşken ziyaretçinin e-posta uygulamasını
  `email` adresine hazır mesajla açar (mailto).
- `docs/assets/data/etkinlikler.js` — etkinlik takvimi (dosyada örnek kayıt şablonu var). Boşken
  "Yaklaşan etkinlik bulunmuyor" yazar.

## Görsel ilkesi

Fotoğraflar **Burst by Shopify** stok arşivinden (ücretsiz ticari lisans); liste ve lisans `GORSEL-KAYNAKLARI.md`'de.
**Yüzü tanınabilen kimse yok:** yapay zekâ ya da stok fark etmez, sitedeki kişi kurucu ya da ekip sanılabildiği için
(müşteri kararı, 18 Eki 2026) yalnız mekân, nesne, el ve arkadan görülen kişi fotoğrafları kullanılır.
Her fotoğrafın köşesinde hizmetin ikonu rozet olarak durur. Emel Özbek fotoğrafı gelince `content/hakkimizda.html`'e eklenir.

## Alan adı, DNS, HTTPS

GoDaddy DNS: `A @` → 185.199.108.153 / .109 / .110 / .111 ve `CNAME www` → `emrecanbuluttt.github.io`.
Kök adres www'ye yönlenir. HTTPS zorunlu (Let's Encrypt, GitHub kendisi yeniler).
Sertifika DNS doğru olduğu hâlde gelmezse: Settings → Pages'te özel alan adını kaldırıp yeniden ekle
(API: `cname` önce `null`, sonra `www.tuksaldanismanlik.com`).

## Açık konular

- **E-posta kutusu yok:** `info@tuksaldanismanlik.com` sitede yayında ama alan adında MX kaydı yok; bu adrese giden
  posta şu an teslim edilemez. GoDaddy'de bir e-posta hizmeti (Microsoft 365, Google Workspace, Zoho ya da
  yönlendirme) kurulunca MX kayıtları DNS'e eklenmeli. Kontrol: `dig +short MX tuksaldanismanlik.com`.
- **Formun doğrudan info@'ya düşmesi:** posta kutusu çalışınca `config.js` → `formEndpoint:
  "https://formsubmit.co/ajax/info@tuksaldanismanlik.com"` yaz, siteden bir deneme mesajı gönder ve info@'ya gelen
  etkinleştirme e-postasındaki bağlantıya tıkla. O zamana kadar form mailto ile çalışır. (Posta kutusu yokken
  formEndpoint yazma: servis etkinleştirme e-postasını teslim edemez.)

- **Referanslar** sayfası gizli (`pages.json` → `hidden`). Taranmış mektuplar gelince `content/referanslar.html`
  içindeki talimata göre ekle ve `hidden`'ı kaldır.
- **İş birliği yapılan markalar:** Mathvivor (www.mathvivor.com bağlantılı), Matematik ve Bilim Festivali (logo),
  Guaj Danışmanlık (logosu ve sitesi yok; yazıyla gösteriliyor). Logolar `docs/assets/img/markalar/`.
- **KVKK metni** yayına almadan önce müşteriyle birlikte gözden geçirilmeli.

## Yapım aşaması moduna dönmek

`_arsiv/yapim-asamasi/docs/` içeriğini `docs/` yerine koy (`CNAME` korunarak) ve push et.
