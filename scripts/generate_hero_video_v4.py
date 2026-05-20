#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 v4 — "The Morning After"

コンセプト: 人物・機械ゼロ。整地済みの解体跡地を朝の光の中、
ドローンが垂直に上昇しながら捉える8秒シングルテイク。
深ネイビー → 真鍮ゴールドのブランドカラーが空のグラデと完全一致。

実行: python3 scripts/generate_hero_video_v4.py
出力: docs/assets/img/hero/hero-main.mp4
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

MODELS = [
    "veo-3.1-generate-preview",
    "veo-3.0-generate-001",
    "veo-3.1-fast-generate-preview",
    "veo-3.0-fast-generate-preview",
]

PROMPT = (
    "[STYLE] Award-winning Japanese architecture cinematography in the style of "
    "Naomi Kawase and Ryuichi Sakamoto's 'Async' film, ultra-slow contemplative tone, "
    "anamorphic 2.39:1 widescreen framing, single continuous take, "
    "no people anywhere in the frame, no machinery or vehicles. "
    "\n\n"
    "[CAMERA] Shot on ARRI Alexa Mini LF with Cooke S7/i 32mm anamorphic lens, "
    "24fps, ProRes 4444 XQ, very subtle anamorphic horizontal lens flares from low sun. "
    "Drone gimbal absolutely stable, zero jitter, zero wobble. "
    "\n\n"
    "[GRADE] Cool blue-to-warm-gold gradient sky. Sky transitions from deep navy "
    "#0F1B2D at the top of frame to warm brass gold #B8935E near horizon. "
    "Subtly desaturated teal-orange grade preserving deep shadows. "
    "Fine film grain emulating Kodak Vision3 250D daylight stock. "
    "\n\n"
    "[LIGHTING] Pre-dawn blue hour transitioning to first golden hour light. "
    "Low key light from screen-right at 5 degree elevation, color temperature warming "
    "from 4500K to 3500K across the shot. Atmospheric haze, light morning mist drifting "
    "horizontally across the foreground. Long soft shadows extending to screen-left. "
    "\n\n"
    "[0:00 - 0:02 OPENING - Ultra-low ground level shot] "
    "Camera at 50cm above ground, facing north toward a rectangular cleared demolition site "
    "freshly graded with crushed gravel base (kurashah-run). Light morning fog drifting "
    "slowly across the gravel surface. In the foreground, the edge of a matte gray opaque "
    "dust-barrier sheet on temporary scaffolding flutters very gently in a slight breeze. "
    "Absolutely no people, no vehicles, no machinery. The cleared lot has clean rectangular "
    "boundaries, freshly compacted, well-finished work. "
    "\n\n"
    "[0:02 - 0:05 SLOW VERTICAL RISE] "
    "Drone begins absolutely smooth vertical ascent at 0.3 m/s, no horizontal drift, "
    "no pan. Camera angle slowly tilts down 15 degrees over 3 seconds. The full rectangular "
    "cleared lot comes into frame. Surrounding it: traditional Japanese suburban houses with "
    "kawara clay tile rooftops, narrow asphalt streets, power lines. Long shadows of utility "
    "poles stretching to screen-left. Still no people, no vehicles. "
    "\n\n"
    "[0:05 - 0:08 AERIAL TOP-DOWN REVEAL] "
    "Drone accelerates vertical ascent to 0.6 m/s while completing tilt down to 75 degrees, "
    "approaching top-down perspective. The complete demolition lot in the foreground "
    "connects visually to the existing neighborhood beyond: rows of kawara-tile rooftops, "
    "tree canopies, residential streets. Morning mist drifts across mid-ground. "
    "Sky fills upper third of frame: deep navy #0F1B2D at top transitioning to brass gold "
    "#B8935E near horizon. Subtle anamorphic lens flare from rising sun off-frame right. "
    "\n\n"
    "[NEGATIVE PROMPT] "
    "No people, no humans, no workers, no faces, no hands, no figures, no silhouettes "
    "of people. No machinery, no excavators, no trucks, no construction vehicles, "
    "no kei-trucks. No readable text, no logos, no brand markings, no signs, "
    "no Japanese characters in frame, no English characters in frame. "
    "No green mesh netting (only matte gray opaque dust-barrier sheeting allowed). "
    "No warping or distortion of buildings. No impossible physics. "
    "No double-exposure or ghosting artifacts. No melting tile roofs. "
    "No flat color blocks in sky (must be smooth gradient). Sharp focus throughout. "
    "No animated cartoon look. No CGI plastic look. No motion blur on buildings. "
    "Accurate Japanese suburban architecture only — kawara clay tile roofs, "
    "two-story wooden frame houses, narrow streets."
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
        return None, f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:500]}"


def main():
    op, used = None, None
    for m in MODELS:
        op, err = kickoff(m)
        if op:
            used = m
            print(f"[OK] kicked off with {m}")
            print(f"     operation: {op}")
            break
        print(f"[FAIL] {m}: {err}", file=sys.stderr)
    if not op:
        sys.exit("All Veo variants failed")

    print(f"\nWaiting for Veo to render (typical 2-8 min)...")
    poll = f"https://generativelanguage.googleapis.com/v1beta/{op}?key={API_KEY}"
    started = time.time()
    while True:
        with urllib.request.urlopen(poll, timeout=60) as r:
            resp = json.loads(r.read())
        if resp.get("done"):
            print(f"[DONE] rendered in {time.time()-started:.0f}s")
            break
        elapsed = time.time() - started
        print(f"  ...polling ({elapsed:.0f}s elapsed)")
        if elapsed > 1500:
            sys.exit("timeout (>25min)")
        time.sleep(20)

    if resp.get("error"):
        sys.exit(f"error: {resp['error']}")

    samples = resp["response"]["generateVideoResponse"]["generatedSamples"]
    uri = samples[0]["video"]["uri"]
    sep = "&" if "?" in uri else "?"
    print("  downloading...")
    with urllib.request.urlopen(f"{uri}{sep}key={API_KEY}", timeout=600) as r:
        data = r.read()
    OUT.write_bytes(data)
    print(f"\n[SAVED] {OUT}")
    print(f"        size: {len(data)//1024} KB")
    print(f"        model: {used}")


if __name__ == "__main__":
    main()
