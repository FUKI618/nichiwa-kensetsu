#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 v3（Veo 3.1で物理整合性UP）
解体現場→ドローン空撮の1テイク。Exa調査ベースのプロンプト。

実行: python3 scripts/generate_hero_video_v3.py
出力: docs/assets/img/hero/hero-main.mp4
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

# Try newest first, fall back if billing/quota issue
MODELS = [
    "veo-3.1-generate-preview",
    "veo-3.0-generate-001",
    "veo-3.1-fast-generate-preview",
]
PROMPT = (
    "A single continuous cinematic take at a Japanese demolition site, golden hour. "
    "IMPORTANT: The scaffolding around the building is fully wrapped in OPAQUE GRAY DUST-AND-NOISE "
    "BARRIER SHEETING (Japanese standard 'boon-bojin sheet'), a solid heavy fabric barrier that "
    "blocks dust and sound from escaping. NOT thin green safety mesh netting. The sheeting is "
    "matte gray or off-white, flat and continuous, completely covering all sides of the scaffolding. "
    "OPENING (ground level): A yellow long-arm hydraulic excavator with grapple attachment "
    "carefully tearing apart the second floor of a partially demolished wooden two-story house. "
    "The building is enclosed by tall scaffolding fully wrapped in matte gray dust barrier sheets. "
    "In the foreground, a Japanese worker in white helmet and navy work jacket holds a water hose, "
    "spraying mist to suppress dust. Wooden beams and roof tiles falling slowly inside the enclosure. "
    "MIDDLE (camera rises): The camera smoothly tilts upward and dollies backward, "
    "rising vertically as if a drone lifting off, revealing the gray-sheeted enclosure from above. "
    "Two more workers come into view, sorting debris into separated piles. "
    "A small dump truck is parked at the edge of the lot. "
    "ENDING (aerial drone): The camera continues rising to a full aerial overhead view, "
    "showing the complete demolition lot wrapped in the gray dust barrier sheeting from above. "
    "Surrounding Japanese residential houses form a quiet neighborhood around the cleared site. "
    "Long shadows from late afternoon sun. Dust particles glinting in warm amber light throughout. "
    "Photorealistic, cinematic 16:9, 8 seconds, smooth continuous camera motion. "
    "Realistic human proportions and movements. Realistic building structure and physics. "
    "No text, no logos, no watermarks, no readable signs, no kanji on equipment, no brand names."
)
OUT = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main.mp4"


def kickoff(model):
    body = {
        "instances": [{"prompt": PROMPT}],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "personGeneration": "allow_all",
        },
    }
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
        f":predictLongRunning?key={API_KEY}"
    )
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read())
        return resp.get("name"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:400]}"


def main():
    op, used = None, None
    for m in MODELS:
        op, err = kickoff(m)
        if op:
            used = m
            print(f"[OK] kicked off with {m}: {op}")
            break
        print(f"[FAIL] {m}: {err}", file=sys.stderr)
    if not op:
        sys.exit("All Veo 3 variants failed")
    print(f"\nWaiting (Veo 3 may take longer than Veo 2, 2-8 min)...")
    poll = f"https://generativelanguage.googleapis.com/v1beta/{op}?key={API_KEY}"
    started = time.time()
    while True:
        with urllib.request.urlopen(poll, timeout=60) as r:
            resp = json.loads(r.read())
        if resp.get("done"):
            print(f"[DONE] in {time.time()-started:.0f}s")
            break
        elapsed = time.time() - started
        print(f"  ...polling ({elapsed:.0f}s)")
        if elapsed > 1200:
            sys.exit("timeout")
        time.sleep(20)
    if resp.get("error"):
        sys.exit(f"error: {resp['error']}")
    samples = resp["response"]["generateVideoResponse"]["generatedSamples"]
    uri = samples[0]["video"]["uri"]
    sep = "&" if "?" in uri else "?"
    print("  downloading...")
    with urllib.request.urlopen(f"{uri}{sep}key={API_KEY}", timeout=300) as r:
        data = r.read()
    OUT.write_bytes(data)
    print(f"[SAVED] {OUT} ({len(data)//1024} KB) using {used}")


if __name__ == "__main__":
    main()
