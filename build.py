#!/usr/bin/env python3
"""
TUKSAL Danışmanlık — static site builder.

  python3 build.py            # content/*.html + templates/page.html -> docs/*.html (+ sitemap, robots)
  python3 build.py --check    # build, then validate links/images/placeholders (exit 1 on problems)

Pages, navigation and site metadata live in content/pages.json.
Each content/<slug>.html holds ONLY the inner HTML of <main>.
"""
import json, re, sys, pathlib, html, datetime

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SITE = ROOT / "docs"
TEMPLATE = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")
CFG = json.loads((CONTENT / "pages.json").read_text(encoding="utf-8"))
S = CFG["site"]
BUILD = datetime.datetime.now().strftime("%Y%m%d%H%M")  # cache-busting ?v= for CSS/JS; changes on every build
CARET = ('<svg class="caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>')


def base(href):
    return href.split("#")[0]


HIDDEN = {f"{p['slug']}.html" for p in CFG["pages"] if p.get("hidden")}


def visible(href):
    return base(href) not in HIDDEN


def render_nav(slug):
    cur = f"{slug}.html"
    out = ['<nav class="nav" id="site-nav" aria-label="Ana menü">', "  <ul>"]
    for item in CFG["nav"]:
        if not visible(item["href"]):
            continue
        kids = item.get("children")
        active = base(item["href"]) == cur or (kids and any(base(i["href"]) == cur for g in kids for i in g["items"]))
        if item.get("cta"):
            out.append(f'    <li><a class="nav-cta" href="{item["href"]}"{" aria-current=\"page\"" if base(item["href"]) == cur else ""}>{html.escape(item["label"])}</a></li>')
            continue
        cls = ' class="' + " ".join(c for c in ["has-sub" if kids else "", "is-active" if active else ""] if c) + '"' if (kids or active) else ""
        cur_attr = ' aria-current="page"' if base(item["href"]) == cur else ""
        if not kids:
            out.append(f'    <li{cls}><a href="{item["href"]}"{cur_attr}>{html.escape(item["label"])}</a></li>')
            continue
        out.append(f'    <li{cls}>')
        out.append(f'      <div class="nav-item-row"><a href="{item["href"]}"{cur_attr}>{html.escape(item["label"])}</a>'
                   f'<button class="nav-toggle" type="button" aria-expanded="false" aria-label="{html.escape(item["label"])} alt menüsü">{CARET}</button></div>')
        out.append('      <ul class="sub">')
        for g in kids:
            out.append(f'        <li class="sub-group">{html.escape(g["group"])}</li>')
            for i in [i for i in g["items"] if visible(i["href"])]:
                ca = ' aria-current="page"' if base(i["href"]) == cur else ""
                out.append(f'        <li><a href="{i["href"]}"{ca}>{html.escape(i["label"])}</a></li>')
        out.append("      </ul>")
        out.append("    </li>")
    out += ["  </ul>", "</nav>"]
    return "\n".join(out)


def render_footer_nav():
    out = []
    for title, items in CFG["footer_nav"].items():
        out.append(f"        <div>\n          <h4>{html.escape(title)}</h4>\n          <ul>")
        for i in [i for i in items if visible(i["href"])]:
            out.append(f'            <li><a href="{i["href"]}">{html.escape(i["label"])}</a></li>')
        out.append("          </ul>\n        </div>")
    return "\n".join(out)


def jsonld(page, canonical):
    home = next(p for p in CFG["pages"] if p["slug"] == "index")
    org = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": S["name"], "alternateName": S["legal_name"], "url": S["url"],
        "image": S["url"].rstrip("/") + "/" + S["og_image"],
        "areaServed": "TR", "description": home["description"],
    }
    if S.get("email"):
        org["email"] = S["email"]
    if S.get("telephone"):
        org["telephone"] = S["telephone"]
    if S.get("address"):
        org["address"] = {"@type": "PostalAddress", **S["address"]}
    org["logo"] = S["url"].rstrip("/") + "/assets/img/logo/tuksal-logo.png"
    return json.dumps(org, ensure_ascii=False)


def build():
    SITE.mkdir(exist_ok=True)
    footer_nav = render_footer_nav()
    built, problems = [], []
    for page in CFG["pages"]:
        slug = page["slug"]
        if page.get("hidden"):
            continue
        src = CONTENT / f"{slug}.html"
        if not src.exists():
            problems.append(f"missing content: content/{slug}.html"); continue
        content = src.read_text(encoding="utf-8")
        content = re.sub(r"[ \t]*<!--.*?-->[ \t]*\n?", "", content, flags=re.S).rstrip() + "\n"  # maintainer notes stay in content/ only
        canonical = S["url"].rstrip("/") + ("/" if slug == "index" else f"/{slug}.html")
        full_title = S["name"] + " — " + page["title"] if slug == "index" else page["title"] + " | " + S["name"]
        out = TEMPLATE
        repl = {
            "{{FULL_TITLE}}": html.escape(full_title), "{{TITLE}}": html.escape(page["title"]),
            "{{DESCRIPTION}}": html.escape(page["description"]), "{{CANONICAL}}": canonical,
            "{{ROBOTS}}": "noindex, follow" if page.get("noindex") else "index, follow",
            "{{OG_IMAGE}}": S["url"].rstrip("/") + "/" + page.get("og_image", S["og_image"]),
            "{{SITE_NAME}}": html.escape(S["name"]), "{{LEGAL_NAME}}": html.escape(S["legal_name"]),
            "{{TAGLINE}}": html.escape(S["tagline"]), "{{EMAIL}}": S["email"],
            "{{ADDRESS}}": "<br>".join(html.escape(l) for l in S.get("address_lines", [])),
            "{{BODY_CLASS}}": page.get("body_class", f"page-{slug}"), "{{NAV}}": render_nav(slug),
            "{{FOOTER_NAV}}": footer_nav, "{{CONTENT}}": content, "{{YEAR}}": str(datetime.date.today().year),
            "{{BUILD}}": BUILD, "{{JSONLD}}": jsonld(page, canonical),
        }
        for k, v in repl.items():
            out = out.replace(k, v)
        if slug != "index":
            out = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", out, flags=re.S)
        if slug == "404":
            out = re.sub(r'\s*<link rel="canonical"[^>]*>', "", out)
            out = re.sub(r'\s*<meta property="og:url"[^>]*>', "", out)
            # GitHub Pages serves 404.html at any depth: make asset and page links root-absolute
            out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|data:)([^"]+)"', r'\1="/\2"', out)
        (SITE / f"{slug}.html").write_text(out, encoding="utf-8")
        built.append(slug)
    # remove stale pages (e.g. pages that were hidden after an earlier build)
    for old in SITE.glob("*.html"):
        if old.stem not in built:
            old.unlink()
    # sitemap + robots
    urls = [S["url"].rstrip("/") + ("/" if p["slug"] == "index" else f"/{p['slug']}.html")
            for p in CFG["pages"] if not p.get("noindex") and not p.get("hidden") and p["slug"] in built]
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {S['url'].rstrip('/')}/sitemap.xml\n", encoding="utf-8")
    return built, problems


def check(built):
    problems = []
    pages = {f"{s}.html" for s in built}
    for slug in built:
        p = SITE / f"{slug}.html"
        txt = p.read_text(encoding="utf-8")
        if "{{" in txt:
            problems.append(f"{slug}.html: unreplaced placeholder {{{{…}}}}")
        # local links
        for href in re.findall(r'(?:href|src)="([^"]+)"', txt):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            target = href.split("#")[0].split("?")[0].lstrip("/")
            if not target:
                continue
            if target.endswith(".html"):
                if target not in pages:
                    problems.append(f"{slug}.html: broken link -> {href}")
            elif not (SITE / target).exists():
                problems.append(f"{slug}.html: missing file -> {href}")
        # anchors on same page
        ids = set(re.findall(r'\sid="([^"]+)"', txt))
        for href in re.findall(r'href="#([^"]+)"', txt):
            if href not in ids and href != "main":
                problems.append(f"{slug}.html: missing anchor #{href}")
        # cross-page anchors
        for tgt, anc in re.findall(r'href="([a-z0-9-]+\.html)#([^"]+)"', txt):
            if tgt in pages:
                tids = set(re.findall(r'\sid="([^"]+)"', (SITE / tgt).read_text(encoding="utf-8")))
                if anc not in tids:
                    problems.append(f"{slug}.html: missing anchor {tgt}#{anc}")
        if "<!--" in txt:
            problems.append(f"{slug}.html: HTML comment shipped to the public page")
        h1 = len(re.findall(r"<h1[\s>]", txt))
        if h1 != 1:
            problems.append(f"{slug}.html: expected exactly one <h1>, found {h1}")
        for m in re.finditer(r"<img\b(?![^>]*\balt=)[^>]*>", txt):
            problems.append(f"{slug}.html: <img> without alt: {m.group(0)[:80]}")
    return problems


if __name__ == "__main__":
    built, problems = build()
    print(f"built {len(built)} pages -> docs/")
    if "--check" in sys.argv:
        problems += check(built)
    for p in problems:
        print("  !", p)
    sys.exit(1 if problems and "--check" in sys.argv else 0)
