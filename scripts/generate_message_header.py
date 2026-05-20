#!/usr/bin/env python3
"""
代表挨拶ページのヘッダー画像を生成。
人物ではなく、業種（解体現場）の cinematic な風景を出す。

実行: python3 scripts/generate_message_header.py
出力: docs/assets/img/message/message-hero.webp
"""
import base64, json, os, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

MODEL = "gemini-2.5-flash-image"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

PROMPT = (
    "Cinematic wide-angle photograph of a Japanese demolition site at golden hour, "
    "moments after the workday has ended. "
    "Cleared, freshly-graded crushed-stone lot in the foreground, "
    "concrete embankment along one side showing decades of weathering and moss patina. "
    "A single yellow long-arm hydraulic excavator parked in the mid-distance, silhouetted, no operator visible, no people anywhere. "
    "Surrounding traditional Japanese suburban architecture: weathered concrete commercial buildings, "
    "kawara clay tile rooftops, narrow asphalt streets, utility poles with overhead power lines. "
    "Light atmospheric mist drifting horizontally at ground level. "
    "Long evening shadows extending across the gravel lot. "
    "Sky fills the upper half: deep navy #0F1B2D at top transitioning to warm brass gold #B8935E along the horizon. "
    "Anamorphic 2.39:1 widescreen aesthetic, "
    "ARRI Alexa Mini LF with Cooke S7/i 32mm anamorphic prime lens, "
    "ProRes 4444, Kodak Vision3 250D film grain. "
    "Subtly desaturated teal-orange color grade, deep shadows preserved, warm highlights. "
    "Subtle horizontal anamorphic lens flare from low sun off-frame right. "
    "Solemn, contemplative, professional tone — the dignity of work completed for the day. "
    "Absolutely no people, no workers, no figures, no faces, no silhouettes of people, no animals, no birds. "
    "No readable text, no readable kanji, no readable katakana, no English text, no logos, no brand markings, no shop signs. "
    "No fisheye distortion, no GoPro look. Photoreal cinematography only. "
    "No machiya alleyways with paper lanterns — only open construction/demolition site setting."
)

OUT = ROOT / "docs" / "assets" / "img" / "message" / "message-hero.webp"
OUT.parent.mkdir(parents=True, exist_ok=True)


def main():
    body = {
        "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:800]}", file=sys.stderr)
        sys.exit(1)

    # Pull inline image data
    parts = resp["candidates"][0]["content"]["parts"]
    for p in parts:
        if "inlineData" in p:
            data = base64.b64decode(p["inlineData"]["data"])
            # Gemini returns PNG by default
            tmp = OUT.with_suffix(".png")
            tmp.write_bytes(data)
            print(f"[OK] saved {tmp} ({len(data)//1024} KB)")
            # Convert PNG → WebP via ffmpeg (much smaller)
            import subprocess
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(tmp), "-c:v", "libwebp", "-quality", "82", str(OUT)],
                check=True, capture_output=True,
            )
            print(f"[OK] converted → {OUT} ({OUT.stat().st_size//1024} KB)")
            tmp.unlink()
            return
    print("[ERR] no image in response", file=sys.stderr)
    print(json.dumps(resp, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    main()
