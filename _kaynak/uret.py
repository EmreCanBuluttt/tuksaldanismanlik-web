#!/usr/bin/env python3
"""Generate docs/index.html (relative paths) and docs/404.html (root-absolute paths) from _kaynak/sayfa.html.
Run after editing _kaynak/sayfa.html:  python3 _kaynak/uret.py"""
import pathlib
root = pathlib.Path(__file__).resolve().parent.parent
out = root / "docs"
src = (root / "_kaynak" / "sayfa.html").read_text(encoding="utf-8")
(out / "index.html").write_text(src.replace("{B}", "").replace("{ROBOTS}", "index, follow").replace('href="" aria-label', 'href="./" aria-label'), encoding="utf-8")
(out / "404.html").write_text(src.replace("{B}", "/").replace("{ROBOTS}", "noindex, follow"), encoding="utf-8")
print("index.html + 404.html written")
