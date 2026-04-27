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
    "[STYLE] Documentary cinematography in the style of Emmanuel Lubezki, "
    "anamorphic 2.39:1 framing, single continuous take. "
    "[CAMERA] Shot on ARRI Alexa Mini LF with Cooke S7/i 32mm anamorphic lens, "
    "24fps, ProRes 4444 RAW, subtle anamorphic flares from the sun. "
    "[GRADE] Subtly desaturated teal-orange color grade, deep shadows preserved, "
    "warm highlights, fine film grain emulating Kodak Vision3 500T. "
    "[LIGHTING] Late golden hour key light from camera-right at 30 degree elevation, "
    "warm 3200K, atmospheric haze with backlit dust particles, "
    "long shadows extending to camera-left. "
    "\n\n"
    "[0:00 - 0:03 OPENING - Low-angle eye-level shot] "
    "A Japanese male worker in his mid-thirties wearing a slightly weathered white helmet, "
    "navy cotton work jacket with reflective stripes, holds an industrial water hose. "
    "He sprays atomized mist toward the demolition area; the mist catches golden sunlight, "
    "refracting into soft rainbow particles. In the right third of the frame, a yellow "
    "long-arm hydraulic excavator with grapple attachment slowly closes on an aged wooden "
    "roof beam (no brand markings on the machine). The foreground shows matte gray "
    "dust-barrier sheeting on scaffolding, slight breeze movement on the fabric. "
    "Background: traditional Japanese suburban rooftops with kawara tiles. "
    "\n\n"
    "[0:03 - 0:05 TRANSITION - Vertical crane lift + dolly back] "
    "The camera lifts vertically 3 meters at 0.6 m/s while dollying back 1.5m. "
    "Smooth Steadicam-like motion, absolutely no jitter or wobble. "
    "Two more workers come into focus in the mid-ground, sorting debris into separated "
    "piles by material: wooden beams, kawara roof tiles, metal fittings. "
    "\n\n"
    "[0:05 - 0:08 AERIAL CLIMAX - Top-down 90 degree drone] "
    "Camera now overhead, drone descending 0.4 m/s straight down. "
    "Reveals the complete demolition lot wrapped in continuous gray dust-barrier sheeting. "
    "A white kei-truck parked at the edge (no brand markings, no logos). "
    "Surrounding traditional Japanese suburban homes with kawara tile roofs, narrow "
    "asphalt streets, power lines. Long evening shadows extending to the right. "
    "\n\n"
    "[NEGATIVE PROMPT] "
    "No warping limbs, no melting wood, no impossible building physics, no readable "
    "text or logos anywhere on equipment or trucks, anatomically correct human proportions, "
    "no extra or missing fingers, no double-exposure ghosting, no AI artifacts, "
    "no blurry edges, sharp focus throughout, no thin green mesh netting "
    "(use only matte gray opaque dust barrier sheeting), no warping faces, "
    "no impossible scaffolding geometry, accurate Japanese residential architecture."
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
