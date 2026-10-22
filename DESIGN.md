# TUKSAL Danışmanlık — page authoring guide (design system + rules)

Static site, no framework. `python3 build.py --check` assembles `content/<slug>.html`
(inner HTML of `<main>` only — no `<html>/<head>/<header>/<footer>`) into `docs/<slug>.html`
using `templates/page.html`, then validates links, anchors, images and `<h1>` count.
Pages, titles, descriptions and navigation live in `content/pages.json`.

## Content rules (non-negotiable)
1. **Single source of truth: `kaynak/musteri-brief.txt`.** Every sentence of the relevant
   brief section must appear on the page (you may reorder, split into sections, add headings,
   and fix obvious typos: "Organizasyoları"→"Organizasyonları", "Hedefimiz.."→"Hedefimiz",
   "Şikâyet" keep, "Kârlılık" keep circumflex). Do not paraphrase away meaning.
2. **No invented facts.** No client names, numbers, years of experience, team sizes, prices,
   certifications, phone numbers, social links, testimonials or biographies that are not in the
   brief. Structural copy (button labels, short lead-ins, section eyebrows, CTA sentences) is fine
   as long as it stays generic and claims nothing new.
3. Site language: **Turkish** (proper Turkish typography: İ/ı, ş, ğ, "Kârlılık", "Hikâye").
   Code comments in English; maintainer instructions aimed at the client (how to add a photo/logo/letter) may be Turkish HTML comments. Bullet lists in the brief become `<ul class="check-list">`.
4. Exactly one `<h1>` per page (inside `.page-hero`). Headings in order (h2 → h3), no skips.
5. Every `<img>` has a meaningful Turkish `alt`. Use only images listed below.
6. Every page ends with a `.cta-band` linking to `iletisim.html`.
7. Relative links only (`yonetici-gelistirme.html`, `assets/img/x.jpg`). Pages: see pages.json.

## Page skeleton (inner pages)
```html
<section class="page-hero">
  <img src="assets/img/hiz-yonetici.jpg" alt="…" loading="eager" fetchpriority="high">
  <div class="container">
    <ol class="breadcrumb" aria-label="Sayfa yolu">
      <li><a href="index.html">Ana Sayfa</a></li>
      <li><a href="egitim-ve-organizasyon.html">Eğitim ve Organizasyon</a></li>
      <li aria-current="page">Yönetici Geliştirme</li>
    </ol>
    <span class="eyebrow">Eğitim ve Organizasyon Programları</span>
    <h1>Yönetici Geliştirme Programı</h1>
    <p class="lead">One-sentence lead taken from the brief.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="prose"> …h2/h3/p from the brief… </div>
      <figure class="feature-media"><img src="assets/img/….jpg" alt="…" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="section section--alt"> … </section>

<section class="section">
  <div class="container">
    <div class="cta-band">
      <div><h2>…</h2><p>…</p></div>
      <div class="btn-row"><a class="btn btn--primary" href="iletisim.html">Bize Ulaşın</a></div>
    </div>
  </div>
</section>
```

## Component vocabulary (all in `docs/assets/css/style.css`)
- Layout: `.container`, `.container--narrow`, `.section` (+ `--alt` grey, `--warm` cream,
  `--navy` dark, `--tight`), `.section-head` (+ `--center`) with `.eyebrow`, `h2`, `.lead`,
  `.grid.grid-2|3|4`, `.split` (+ `--reverse`), `.prose` (max 72ch), `.divider`.
- Utilities: `.mt-1/.mt-2/.mt-3`, `.mb-0/.mb-2`, `.text-lg`, `.text-center`, `.pill-row` (+ `--center`), `.btn-row--center`, `.formula > .plus`, `.callout--center`, `.ref-card--placeholder`. `.section--navy` recolors `.lead`/`.tagline` automatically. No inline `style=` attributes.
- Text: `.eyebrow`, `.lead`, `.tagline` (+ `--gold`) for the brief's closing slogans,
  `.callout` / `.callout--quote` for a highlighted sentence, `.pill` (+ `--navy`, `--green`), `.notice`.
- Lists: `.check-list` (2-col checkmarks), `.steps` (numbered `<ol>` of `<li><h3>…</h3><p>…</p></li>`).
- Cards: `.card` (`.card-media > img`, `.card-body > h3, p, a.link-arrow`), `a.card.card--link`,
  `.icon-card` (`.icon > svg`, `h3`, `p`), `.stat` inside `.stats`.
- Media: `.feature-media` (+ `--tall`) wrapping `<img>`; optional `.badge` with `<strong>`.
- Buttons: `.btn` + `--primary` (gold), `--navy`, `--outline`, `--ghost` (on dark), `--sm`; `.btn-row`; `.link-arrow`.
- Bands: `.cta-band`, `.quotes > .quote > p` (navy section), `.logo-strip > .logo-card`
  (+ `--placeholder`), `.ref-grid > button.ref-card` (+ `#lightbox` dialog), `.testimonial`.
- Page-specific: `.anchor-nav` (pill links to `#id`s) + `.service-block` (id'd sections with `.split`),
  `.calendar-layout` with `#calendar` and `#event-list` (JS renders from `assets/data/etkinlikler.js`;
  `data-limit="3"` limits, `data-show-past="true"` includes past), `.contact-grid`, `.contact-list`,
  `.form` (`#contact-form`, `.field`, `.form-row`, `.form-status`), `.map-embed > iframe#map-frame`,
  `.error-page`.
- Animation: add `class="reveal"` to cards/blocks that should fade in (never on the hero or h1).

## Icons (inline SVG, 24px grid, stroke) — copy as needed
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>  <!-- users -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M23 6l-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/></svg>  <!-- trending-up -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="6"/><path d="M15.5 13l1.5 9-5-3-5 3 1.5-9"/></svg>  <!-- award -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>  <!-- target -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>  <!-- calendar -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16v16H4z"/><path d="M4 4l8 8 8-8"/></svg>  <!-- mail -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>  <!-- map-pin -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.35 1.85.59 2.81.72A2 2 0 0 1 22 16.92z"/></svg>  <!-- phone -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>  <!-- edit -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>  <!-- check-square -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>  <!-- message -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3 7h7l-5.5 4.5L18.5 22 12 17.5 5.5 22l2-8.5L2 9h7z"/></svg>  <!-- star -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>  <!-- book -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="M7 15l4-4 4 4 5-6"/></svg>  <!-- chart -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/></svg>  <!-- heart -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>  <!-- shield -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>  <!-- clock -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 7h-9M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/></svg>  <!-- sliders -->
```

## Images — NO PHOTOS OF PEOPLE (client decision, 18 Oct 2026)

The site ships without photos. Heroes use the CSS brand background (navy + outlined logo mark);
cards use `<div class="card-media card-visual" aria-hidden="true"><span class="cv-icon"><svg…/></span></div>`
and panels use `<figure class="feature-media feature-visual" aria-hidden="true"><span class="cv-icon">…</span></figure>`.
Never add AI-generated people (they get mistaken for the founder/team). Real client photos only.

### Legacy image list (archived in `_gorsel-arsiv/`, not published)
Hero 16:9: `hero-1.jpg` … `hero-4.jpg` (home slider; may also serve as a `.page-hero` cover, never inside a 3:2 `.feature-media`).
3:2: `hiz-sempozyum.jpg`, `hiz-bireysel.jpg`, `hiz-egitim-aktivite.jpg`, `hiz-yonetici.jpg`,
`hiz-musteri.jpg`, `hiz-ekip.jpg`, `hiz-marka.jpg`, `hiz-pazarlama-strateji.jpg`,
`hiz-satis-cozumleme.jpg`, `hiz-musteri-deneyimi.jpg`, `hiz-satis-sonrasi.jpg`, `hiz-ik.jpg`,
`hiz-isgucu-karlilik.jpg`, `hakkimizda-ofis.jpg`, `etkinlik.jpg`, `referans.jpg`.
No photo of Emel Özbek exists yet — use the `.founder-placeholder` block (see hakkimizda spec), never
a generated portrait. Reference letters are not scanned yet — use `.doc-placeholder` thumbnails.

## Tone
Professional, warm, confident; short paragraphs; the brief's closing slogans
("Öğrenin. Deneyimleyin. Gelişin. Performansınızı yükseltin.") go in `.tagline` or `.callout`.
