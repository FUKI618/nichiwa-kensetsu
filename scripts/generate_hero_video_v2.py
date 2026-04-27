#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 v2（解体風景→ドローン空撮の1テイク）
Exa調査による日本の解体プロセスのリアル描写を反映。
text-to-video で 1本完結（カメラが地上→上昇→俯瞰へ単一テイク）。

実行: python3 scripts/generate_hero_video_v2.py
出力: docs/assets/img/hero/hero-main.mp4
"""
import json, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

MODEL = "veo-2.0-generate-001"

# Single-take cinematic camera motion: ground-level demolition → tilt up + dolly back → aerial drone
PROMPT = (
    "A single continuous cinematic take at a Japanese demolition site, golden hour. "
    "OPENING (ground level): A yellow long-arm hydraulic excavator with grapple attachment "
    "carefully tearing apart the second floor of a partially demolished wooden two-story house. "
    "In the foreground, a Japanese worker in white helmet and navy work jacket holds a water hose, "
    "spraying mist to suppress dust. Wooden beams and roof tiles falling slowly. "
    "Green safety netting visible on scaffolding around the building. "
    "MIDDLE (camera rises): The camera smoothly tilts upward and dollies backward, "
    "rising vertically as if a drone lifting off, revealing more of the site from a slight elevation. "
    "Two more workers come into view, sorting debris into separated piles "
    "(wood, roof tiles, metal). A small dump truck is parked at the edge of the lot. "
    "ENDING (aerial drone): The camera continues rising to a full aerial overhead view, "
    "now showing the entire demolition lot from above. Surrounding Japanese residential houses "
    "form a quiet neighborhood around the cleared site. Long shadows from late afternoon sun. "
    "Dust particles glinting in warm amber light throughout. "
    "Photorealistic, cinematic 16:9, 8 seconds, smooth continuous camera motion. "
    "No text, no logos, no watermarks, no readable signs, no kanji on equipment."
)
OUT = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main.mp4"


def main():
    body = {
        "instances": [{"prompt": PROMPT}],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "personGeneration": "allow_adult",
        },
    }
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}"
        f":predictLongRunning?key={API_KEY}"
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        kickoff = json.loads(r.read())
    op = kickoff["name"]
    print(f"[OK] kicked off: {op}")
    print("Waiting for Veo 2 (1-5 min)...")
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
        if elapsed > 900:
            sys.exit("timeout")
        time.sleep(15)
    if resp.get("error"):
        sys.exit(f"error: {resp['error']}")
    samples = resp["response"]["generateVideoResponse"]["generatedSamples"]
    uri = samples[0]["video"]["uri"]
    sep = "&" if "?" in uri else "?"
    download_url = f"{uri}{sep}key={API_KEY}"
    print("  downloading...")
    with urllib.request.urlopen(download_url, timeout=300) as r:
        data = r.read()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"[SAVED] {OUT} ({len(data)//1024} KB)")


if __name__ == "__main__":
    main()
