#!/usr/bin/env python3
"""
セクションに合った画像を3枚生成。

1. services/demolition.webp 差し替え — 「書類を持つ手」では弱い。
   実際の解体作業を映す editorial wide shot に。
2. strengths-hero.webp 新規 — /strengths/ 専用。
   強み(技術・組織・規律) を象徴する建築事務所的なシーン。
3. sustainability-hero.webp 新規 — /sustainability/ 専用。
   分別された建材廃棄物の整然とした dawn ドキュメンタリーショット。

実行: python3 scripts/generate_section_images.py
"""
import base64, json, sys, urllib.request, urllib.error, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

MODEL = "gemini-2.5-flash-image"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

COMMON_NEGATIVE = (
    " No readable text, no readable kanji or katakana, no English text, "
    "no logos, no brand markings on machinery, no people's faces visible, "
    "no flying objects in frame (drone/quadcopter/helicopter). "
    "Photoreal cinematography only — no CGI plastic look, no cartoon, "
    "no anime. No fisheye, no GoPro look. Sharp focus. "
    "No film stock simulation, no printed edge markings inside the frame, "
    "no frame numbers like '0B8935E', no celluloid borders. "
    "Color palette muted with deep navy #111111 in shadows and a narrow "
    "warm rust #A14A2B band only where the sun touches."
)


JOBS = [
    {
        "out": "docs/assets/img/services/demolition.webp",
        "prompt": (
            "Cinematic wide-angle documentary photograph of a Japanese demolition "
            "site in active operation. Foreground: a large yellow long-arm "
            "hydraulic excavator (no brand markings) reaching into the partially "
            "demolished mid-rise reinforced-concrete building, gripping debris "
            "with its grapple attachment. Mid-distance: matte gray opaque "
            "dust-barrier sheeting on scaffolding contains the work area. "
            "Fine dust particles drift gently in late afternoon golden-hour light "
            "from screen right. Surrounding context: traditional Japanese "
            "suburban houses with kawara tile roofs visible just beyond the "
            "barriers, narrow asphalt streets, utility poles with overhead lines. "
            "No people visible (operator behind tinted cab). Sky transitions from "
            "deep navy #111111 at top to a thin warm rust #A14A2B band at horizon. "
            "Subtle desaturated palette, deep shadows preserved, anamorphic 2.39:1 "
            "framing. ARRI Alexa Mini LF with Cooke S7/i 32mm prime lens aesthetic. "
            "Solemn, professional, editorial-magazine quality." + COMMON_NEGATIVE
        ),
    },
    {
        "out": "docs/assets/img/strengths/strengths-hero.webp",
        "prompt": (
            "Cinematic wide-angle editorial photograph of a Japanese demolition "
            "and construction site at first golden-hour light, viewed from a "
            "slightly elevated perspective. The scene shows ORGANIZATION and "
            "CRAFT: neatly arranged stacks of separated demolition debris sorted "
            "by material (concrete blocks, twisted rebar pile, kawara roof tiles "
            "in a separate heap, wooden beams stacked apart), a clean perimeter "
            "of matte gray dust-barrier sheets, several yellow long-arm "
            "excavators parked in a row at rest (no operators), and a small "
            "stack of safety helmets on a sawhorse table. The environment is "
            "EMPTY OF PEOPLE but full of evidence of disciplined, careful work. "
            "Background: surrounding Japanese suburban townscape with kawara "
            "rooftops, utility poles. Sky: deep navy #111111 above, narrow "
            "rust #A14A2B band at horizon. Long horizontal shadows. "
            "Documentary photojournalism feel, editorial magazine quality, "
            "anamorphic 2.39:1, ARRI Alexa cinematography aesthetic. "
            "Solemn, professional, conveys CRAFT and DISCIPLINE." + COMMON_NEGATIVE
        ),
    },
    {
        "out": "docs/assets/img/sustainability/sustainability-hero.webp",
        "prompt": (
            "Cinematic wide-angle documentary photograph at pre-dawn blue hour, "
            "showing a fully cleared and graded post-demolition lot in suburban "
            "Japan. The site is IMPECCABLY clean — freshly crushed-stone surface "
            "perfectly raked, matte gray dust-barrier sheeting standing upright "
            "in tidy panels along the perimeter, a single neatly-stacked pile of "
            "sorted concrete chunks ready for recycling pickup at one edge. "
            "Light morning mist drifts horizontally across the lot. The "
            "surrounding traditional Japanese homes with kawara tile roofs are "
            "INTACT and undisturbed — the demolition work has finished respectfully. "
            "Absolutely no people, no machinery in the frame (work is done). "
            "Sky fills upper 60%: deep navy #111111 transitioning to a narrow "
            "rust #A14A2B band along the horizon. Long blue shadows. "
            "The mood: STEWARDSHIP, RESPECT, RESPONSIBILITY — the site has been "
            "returned to the community in better condition than industrial work "
            "norms suggest. Documentary photojournalism, editorial magazine "
            "quality, anamorphic 2.39:1." + COMMON_NEGATIVE
        ),
    },
]


def call_gemini(prompt: str) -> bytes:
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.loads(r.read())
    parts = resp["candidates"][0]["content"]["parts"]
    for p in parts:
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"])
    raise RuntimeError("no image in response: " + json.dumps(resp)[:500])


def png_to_webp(png_path: Path, webp_path: Path, quality: int = 82) -> None:
    subprocess.run(
        ["cwebp", "-q", str(quality), str(png_path), "-o", str(webp_path)],
        check=True, capture_output=True,
    )
    png_path.unlink()


def main():
    for job in JOBS:
        out = ROOT / job["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        png = out.with_suffix(".png")
        try:
            data = call_gemini(job["prompt"])
        except urllib.error.HTTPError as e:
            print(f"[FAIL] {job['out']}: HTTP {e.code} {e.read()[:300].decode(errors='replace')}", file=sys.stderr)
            continue
        png.write_bytes(data)
        png_to_webp(png, out)
        print(f"✓ {job['out']} ({out.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
