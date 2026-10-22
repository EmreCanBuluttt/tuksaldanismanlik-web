#!/usr/bin/env python3
"""
TUKSAL Danışmanlık site imagery generator (Google Gemini / AI Studio).

Usage:
  python3 tools/gorsel-uret.py --list            # list prompt keys
  python3 tools/gorsel-uret.py --all             # generate everything -> site/assets/img/_raw/<key>.png
  python3 tools/gorsel-uret.py hero-1 hiz-ik     # only these
  python3 tools/gorsel-uret.py --all --model gemini-3-pro-image

API key: env GEMINI_API_KEY or ~/.config/moredtf/gemini.key (never printed).
Images contain NO text — quotes/titles are overlaid in HTML so the client can edit them.
Post-process (crop/resize/jpeg) is done by tools/gorsel-isle.py.
"""
import argparse, base64, json, os, sys, pathlib, urllib.request, concurrent.futures

HERE = pathlib.Path(__file__).resolve().parent.parent
OUT = HERE / "site" / "assets" / "img" / "_raw"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
DEFAULT_MODEL = "gemini-3.1-flash-image"

STYLE = (
    "Photorealistic editorial corporate photograph, shot on a full-frame camera with a 35mm lens, "
    "natural soft daylight, shallow depth of field, calm and premium mood. Colour grading: deep navy blue "
    "and warm neutral tones with subtle warm-gold highlights, muted and cohesive palette. "
    "Turkish / Mediterranean European professionals aged 28-50, smart business-casual attire, authentic "
    "candid expressions, no staged stock-photo grins. Modern architecture, clean spaces. "
    "ABSOLUTELY NO text, letters, numbers, logos, signs, watermarks, screens with readable words, "
    "or brand marks anywhere in the image. No distorted hands or faces. High resolution, ultra sharp."
)
WIDE = "Composition: WIDE 16:9 landscape, cinematic, with negative space on the left third for a headline overlay. "
STD = "Composition: 3:2 landscape, subject slightly off-centre. "

PROMPTS = {
  # ---- home hero slides (one per quote; quote text is overlaid by HTML) ----
  "hero-1": WIDE + "A confident female executive in her forties leading a strategy discussion at the head of a "
            "long table in a bright glass-walled boardroom; colleagues listening, city view softly blurred behind. " + STYLE,
  "hero-2": WIDE + "A manager walking out of an office building with her team into a sunlit courtyard, "
            "laughing and talking, jackets over shoulders, leaving the meeting room behind. " + STYLE,
  "hero-3": WIDE + "A diverse team of six professionals building a tall structure together from wooden blocks on a "
            "workshop table, focused and collaborative, hands in the frame, warm daylight loft space. " + STYLE,
  "hero-4": WIDE + "A business team in a huddle celebrating a completed team challenge outdoors, arms raised, "
            "genuine joy, late-afternoon golden light, modern campus lawn. " + STYLE,
  # ---- service pages ----
  "hiz-sempozyum": STD + "A large modern congress hall seen from the back rows: full audience, a speaker on a "
            "wide stage lit in blue and warm white, elegant stage design without any lettering. " + STYLE,
  "hiz-bireysel": STD + "One-to-one coaching session: a coach and a young professional talking at a small table "
            "by a window, open notebook, coffee cups, encouraging atmosphere. " + STYLE,
  "hiz-egitim-aktivite": STD + "Interactive corporate workshop: small groups around tables covered with colourful "
            "blank sticky notes and markers, a facilitator standing, energetic and playful mood. " + STYLE,
  "hiz-yonetici": STD + "A senior manager in his forties giving calm, clear feedback to two team members "
            "standing beside a glass wall covered in blank sticky notes, leadership presence. " + STYLE,
  "hiz-musteri": STD + "A warm handshake between a consultant and a client across a bright showroom counter, "
            "both smiling with genuine trust, soft daylight. " + STYLE,
  "hiz-ekip": STD + "A team planning session around a wall-mounted board with blank colourful cards arranged "
            "in columns, a woman moving a card while colleagues discuss, organised and focused. " + STYLE,
  "hiz-marka": STD + "A brand strategist arranging a mood board of fabric swatches, blank colour cards and "
            "printed photographs on a large white table in a design studio, hands and materials only. " + STYLE,
  "hiz-pazarlama-strateji": STD + "Two professionals sketching a marketing funnel and abstract charts with markers "
            "on a large glass whiteboard, shapes and arrows only, no letters, backlit by daylight. " + STYLE,
  "hiz-satis-cozumleme": STD + "A sales team reviewing abstract bar and line charts printed on paper spread over a "
            "desk, one person pointing at a rising line, tablets and coffee, analytical mood. " + STYLE,
  "hiz-musteri-deneyimi": STD + "A delighted customer receiving a beautifully wrapped package from a friendly "
            "staff member in a boutique, eye contact and warmth, premium retail interior. " + STYLE,
  "hiz-satis-sonrasi": STD + "A friendly customer-relations specialist wearing a headset, smiling during a "
            "follow-up call at a tidy desk with a small plant, blurred open office behind. " + STYLE,
  "hiz-ik": STD + "A job interview in a bright meeting room: an HR manager and a candidate shaking hands "
            "across the table, a printed CV face-down, welcoming atmosphere. " + STYLE,
  "hiz-isgucu-karlilik": STD + "An operations manager walking through a clean, well-organised modern light "
            "industrial workspace with a tablet, workers efficiently moving in the background. " + STYLE,
  # ---- other ----
  "hakkimizda-ofis": STD + "A modern consulting agency office in Izmir: open space with warm wood, navy accents, "
            "plants, a small team collaborating at a large table, Aegean daylight through big windows. " + STYLE,
  "etkinlik": STD + "Participants registering and networking in the bright foyer of a conference venue, "
            "lanyards without readable text, coffee, animated conversations. " + STYLE,
  "referans": STD + "Close-up of hands holding an elegant letter on cream paper with an embossed but "
            "unreadable seal, blurred office desk behind, warm light. " + STYLE,
}


def api_key():
    k = os.environ.get("GEMINI_API_KEY")
    if k:
        return k.strip()
    p = pathlib.Path.home() / ".config/moredtf/gemini.key"
    if p.exists():
        return p.read_text().strip()
    sys.exit("GEMINI_API_KEY not found (env or ~/.config/moredtf/gemini.key).")


def find_image(obj):
    if isinstance(obj, dict):
        mime = obj.get("mime_type") or obj.get("mimeType") or ""
        data = obj.get("data")
        if isinstance(data, str) and str(mime).startswith("image/"):
            return data
        for v in obj.values():
            r = find_image(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_image(v)
            if r:
                return r
    return None


def generate(name, prompt, model, key):
    body = json.dumps({"model": model, "input": [{"type": "text", "text": prompt}]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        return f"FAIL {name}: HTTP {e.code} {e.read()[:300].decode(errors='replace')}"
    except Exception as e:
        return f"FAIL {name}: {e}"
    b64 = find_image(payload)
    if not b64:
        return f"FAIL {name}: no image in response -> {json.dumps(payload)[:300]}"
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{name}.png"
    dest.write_bytes(base64.b64decode(b64))
    return f"OK   {name}  ({dest.stat().st_size // 1024} KB)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--missing", action="store_true", help="only keys without a raw file yet")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    if a.list:
        print("\n".join(PROMPTS)); return
    jobs = {}
    if a.all:
        jobs.update(PROMPTS)
    if a.missing:
        jobs.update({k: v for k, v in PROMPTS.items() if not (OUT / f"{k}.png").exists()})
    for n in a.names:
        if n not in PROMPTS:
            sys.exit(f"unknown key: {n}")
        jobs[n] = PROMPTS[n]
    if not jobs:
        ap.print_help(); return
    key = api_key()
    print(f"model={a.model} images={len(jobs)} jobs={a.jobs}", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(generate, n, p, a.model, key) for n, p in jobs.items()]
        for f in concurrent.futures.as_completed(futs):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
