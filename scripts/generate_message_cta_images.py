#!/usr/bin/env python3
"""
message-hero.webp と cta-bg.webp を、ページのトーンに合わせて再生成。

- message-hero.webp (/company/ page hero) — 企業情報 = 代表挨拶+会社概要+人。
  現在: 重機が住宅街を一台で歩く解体絵 → 「会社/人」感が弱い。
  新規: dawn の作業前ヤード、図面が広げられた折り畳みテーブル、ヘルメット数個、
        後ろ姿の作業着の人物が現場へ歩き出す影 — TEAM/TRUST/会社の朝。

- cta-bg.webp (/contact.html page hero) — お問い合わせ = 相談しやすい入口。
  現在: 廃墟と作業員のシルエット、夕日 → 重く憂愁的すぎる。
  新規: 明るい日中、住宅街の整った道、青空、新緑、清潔感のあるダストバリア越しに
        住宅が見える、開放的でフレンドリーな「ご相談ください」のトーン。

実行: python3 scripts/generate_message_cta_images.py
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
    "no frame numbers, no celluloid borders. No torn-down ruined buildings "
    "in foreground. No machiya, no narrow alleys, no red paper lanterns."
)

JOBS = [
    {
        "out": "docs/assets/img/message/message-hero.webp",
        "prompt": (
            "Cinematic wide-angle editorial photograph at early dawn first-light "
            "in a Japanese demolition company's outdoor staging yard. Composition: "
            "a folding work table center-frame with a large rolled-out site plan "
            "weighted by a thermos and a clipboard. Three matte white construction "
            "hard hats arranged neatly on the table. Behind the table, mid-distance, "
            "the back of one figure in clean blue-grey workwear is walking gently "
            "away toward a row of parked yellow long-arm excavators at rest. "
            "ABSOLUTELY no faces visible — only the back of the walking figure, "
            "framed small in the composition. Background: matte gray dust-barrier "
            "sheets neatly hung along the lot perimeter, suburban Japanese kawara "
            "rooftops just beyond. Sky: deep navy #111111 above transitioning to "
            "narrow warm rust #A14A2B band at horizon, light morning haze. "
            "The mood is TEAM, TRUST, MORNING BRIEFING — the company beginning "
            "its day together. Documentary photojournalism, editorial magazine "
            "quality, anamorphic 2.39:1, ARRI Alexa cinematography aesthetic. "
            "Muted desaturated palette, long shadows, dignified." + COMMON_NEGATIVE
        ),
    },
    {
        "out": "docs/assets/img/cta/cta-bg.webp",
        "prompt": (
            "Cinematic wide-angle editorial photograph at clear bright mid-morning "
            "on a tidy Japanese suburban residential street in Sakai, Osaka. "
            "Center-frame: a single uniformed worker in clean blue-grey workwear "
            "and white hard hat standing at a polite respectful distance, "
            "shown from behind or three-quarter back angle, holding a clipboard "
            "and a tape measure, looking attentively toward a modest two-story "
            "Japanese house. The body language is OPEN and ATTENTIVE — ready to "
            "listen, not imposing. ABSOLUTELY no face visible. Background: the "
            "well-kept residential house with kawara tile roof, small front garden, "
            "neighboring homes visible further down the quiet street. Soft natural "
            "daylight, mild blue sky with thin cirrus clouds. Subtle accents of "
            "green from street plantings. Mood: WELCOMING CONSULTATION — first "
            "polite visit, easy to approach. Documentary photojournalism, "
            "editorial magazine quality, anamorphic 2.4:1 framing favoring "
            "horizontal width. Muted but warm palette — soft daylight not "
            "harsh sun. NOT solemn or dramatic. NOT sunset. NOT silhouette." + COMMON_NEGATIVE
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
