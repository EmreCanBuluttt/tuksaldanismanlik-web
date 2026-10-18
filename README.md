# tuksaldanismanlik.com — "yapım aşamasında" sayfası

TUKSAL Danışmanlık (Emel Özbek Eğitim ve Proje Ajansı) için geçici tanıtım sayfası.
Asıl site hazır olana kadar `www.tuksaldanismanlik.com` adresinde yayında kalır.

- **Barındırma:** GitHub Pages, bu deponun `main` dalındaki `docs/` klasörü. Her `git push` 1-2 dakikada yayına çıkar.
- **Alan adı:** GoDaddy. Gerekli DNS kayıtları aşağıda.
- **Bağımlılık yok:** fontlar (`docs/assets/fonts`, SIL OFL) ve görseller depoda; dış servise istek atılmaz.

## Düzenleme

1. `_kaynak/sayfa.html` dosyasını düzenle (metin, iletişim satırları).
2. `python3 _kaynak/uret.py` çalıştır. `docs/index.html` ve `docs/404.html` üretilir.
3. `git commit -am "..." && git push`.

E-posta ve telefon satırları `_kaynak/sayfa.html` içinde yorum olarak hazır bekliyor.
Çalışan adres/numara netleşince yorumu açıp değerleri yazman yeterli.

## GoDaddy DNS kayıtları

| Tür | Ad | Değer |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | emrecanbuluttt.github.io |

GoDaddy'nin varsayılan "Parked" A kaydı ve `www → @` CNAME kaydı bunlarla değiştirilir.
`_dmarc` gibi diğer kayıtlara dokunulmaz. Kök alan adı (`tuksaldanismanlik.com`) GitHub tarafından
otomatik olarak `https://www.tuksaldanismanlik.com` adresine yönlendirilir.

## Asıl siteye geçiş

Asıl site `TuksalWeb/site/` klasöründe (ayrı, statik). Hazır olunca o klasörün içeriği
`docs/` yerine konur (`CNAME` dosyası korunarak) ve push edilir. DNS değişmez.

## Görsel ilkesi

Kapakta ve paylaşım görselinde (`docs/assets/img/paylasim.jpg`) **insan yok**: arka plan logodaki işaretten
türetilmiş bir grafik. Yapay zekâyla üretilmiş kişiler kurucu ya da ekip sanılabildiği için kullanılmıyor
(müşteri kararı, 18 Eki 2026). Gerçek fotoğraf gerekiyorsa yalnız müşterinin kendi fotoğrafları.

## Açık konular (18 Eki 2026)

- **E-posta yok.** Brief'teki `destek@mcpdanismanlik.com` adresinin alan adı (`mcpdanismanlik.com`)
  hiç kayıtlı değil; bu adrese giden posta geri döner. `tuksaldanismanlik.com` için de MX kaydı yok.
  Bu yüzden sayfada e-posta gösterilmiyor. Çalışan bir adres (ör. GoDaddy/Google Workspace ile
  `info@tuksaldanismanlik.com`) kurulunca `_kaynak/sayfa.html` içindeki yorumu aç.
  Asıl sitedeki (`TuksalWeb/site/assets/js/config.js`, `content/pages.json`) aynı adres de düzeltilmeli.
- **Telefon** briefte yok; numara gelince aynı şekilde yorumu aç.
- **HTTPS:** 18 Eki 2026'dan beri açık ve zorunlu (Let's Encrypt, `www` + kök alan adı, GitHub kendisi yeniler).
  Sertifika DNS doğru olduğu hâlde gelmezse: Settings → Pages'te özel alan adını kaldırıp yeniden ekle
  (API: `cname` önce `null`, sonra `www.tuksaldanismanlik.com`) — 18 Eki'de sertifika bununla anında çıktı.
- İsteğe bağlı güvenlik: GitHub → Settings → Pages → "Verified domains" ile alan adını hesaba doğrula
  (GoDaddy'ye bir TXT kaydı eklenir); başka bir GitHub hesabının alan adını sahiplenmesini engeller.
