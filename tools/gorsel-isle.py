#!/usr/bin/env python3
"""
Post-process raw Gemini PNGs into web-ready JPEGs.
  site/assets/img/_raw/<key>.png  ->  site/assets/img/<key>.jpg
hero-*  : 16:9 centre crop, 1920px wide
others  : 3:2 centre crop, 1400px wide
og-image: hero-1 cropped to 1200x630
Usage: python3 tools/gorsel-isle.py
"""
import pathlib, sys
from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).resolve().parent.parent
RAW = HERE / "site" / "assets" / "img" / "_raw"
OUT = HERE / "site" / "assets" / "img"


def crop_to(img, ratio, width):
    w, h = img.size
    target = ratio
    if w / h > target:
        nw = int(h * target); box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = int(w / target); box = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
    img = img.crop(box)
    if img.size[0] > width:
        img = img.resize((width, int(width / target)), Image.LANCZOS)
    return img


def main():
    if not RAW.exists():
        sys.exit("no raw images")
    for p in sorted(RAW.glob("*.png")):
        img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        key = p.stem
        src = img.size
        if key.startswith("hero-"):
            out = crop_to(img, 16 / 9, 1920)
        else:
            out = crop_to(img, 3 / 2, 1400)
        dest = OUT / f"{key}.jpg"
        out.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
        print(f"{key:24s} {src[0]}x{src[1]} -> {out.size[0]}x{out.size[1]}  {dest.stat().st_size // 1024} KB")
        if key == "hero-1":
            og = crop_to(img, 1200 / 630, 1200)
            og.save(OUT / "og-image.jpg", "JPEG", quality=82, optimize=True)
            print(f"{'og-image':24s} -> {og.size[0]}x{og.size[1]}")


if __name__ == "__main__":
    main()
