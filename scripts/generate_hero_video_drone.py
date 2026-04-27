#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 #2（ドローン視点）
text-to-video で全く新規の俯瞰ショットを生成。

実行: python3 scripts/generate_hero_video_drone.py
出力: docs/assets/img/hero/hero-02.mp4
"""
import base64, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

MODEL = "veo-2.0-generate-001"
PROMPT = (
    "Aerial cinematic drone shot slowly descending and rotating over a "
    "Japanese demolition site at golden hour. Looking down at a partially "
    "demolished wooden two-story house, surrounding scaffolding with green "
    "safety nets, a yellow excavator parked nearby. Three workers in white "
    "helmets and navy work jackets visible from above, looking up. "
    "Warm amber sunlight, dust softly drifting, long shadows. "
    "Smooth gentle camera tilt and rotation. "
    "Photorealistic, no text, no logos, no watermarks, no readable signs. "
    "16:9 cinematic, 8 seconds, smooth motion."
)
OUT = ROOT / "docs" / "assets" / "img" / "hero" / "hero-02.mp4"


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
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        kickoff = json.loads(r.read())
    op = kickoff["name"]
    print(f"[OK] kicked off: {op}")
    print("Waiting for video generation (1-5 min)...")
    poll_url = f"https://generativelanguage.googleapis.com/v1beta/{op}?key={API_KEY}"
    started = time.time()
    while True:
        with urllib.request.urlopen(poll_url, timeout=60) as r:
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
    print(f"  downloading...")
    with urllib.request.urlopen(download_url, timeout=300) as r:
        data = r.read()
    OUT.write_bytes(data)
    print(f"[SAVED] {OUT} ({len(data)//1024} KB)")


if __name__ == "__main__":
    main()
