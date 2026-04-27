#!/usr/bin/env python3
"""
日和建設 ヒーロー動画生成（Gemini API / Veo 3）
hero-01.webp の世界観を image-to-video で動画化。

実行: python3 scripts/generate_hero_video.py
出力: docs/assets/img/hero/hero-01.mp4
"""
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                break

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found", file=sys.stderr)
    sys.exit(1)

# Try Veo 3 first, fallback to Veo 2 if 403/404
MODELS_TO_TRY = ["veo-3.0-generate-preview", "veo-3.0-fast-generate-preview", "veo-2.0-generate-001"]
PROMPT = (
    "Cinematic slow shot of a Japanese demolition site at golden hour. "
    "A yellow long-arm excavator slowly extending its arm toward a partially "
    "demolished wooden two-story house. Dust softly drifting in warm sunlight. "
    "Three workers in white helmets and navy work jackets standing at distance, "
    "looking on respectfully. Gentle camera dolly-forward motion. "
    "Moody dark navy sky transitioning to amber. Photorealistic, "
    "no text, no logos, no watermarks, no readable signs. "
    "16:9 cinematic, smooth motion."
)

HERO_IMG = ROOT / "docs" / "assets" / "img" / "hero" / "hero-01.webp"
OUT_MP4 = ROOT / "docs" / "assets" / "img" / "hero" / "hero-01.mp4"


def post_json(url: str, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(url: str) -> dict:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_bytes(url: str) -> bytes:
    """Download from a URI which may include API key as query."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def try_kickoff(model: str) -> tuple[str, dict] | None:
    """Submit generation request, return (operation_name, full_response)."""
    img_b64 = base64.b64encode(HERO_IMG.read_bytes()).decode("ascii")
    body = {
        "instances": [
            {
                "prompt": PROMPT,
                "image": {"bytesBase64Encoded": img_b64, "mimeType": "image/webp"},
            }
        ],
        "parameters": {
            "aspectRatio": "16:9",
            "durationSeconds": 8,
            "personGeneration": "allow_adult",
        },
    }
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predictLongRunning"
        f"?key={API_KEY}"
    )
    try:
        resp = post_json(url, body)
        op_name = resp.get("name")
        if op_name:
            print(f"[OK] kicked off with {model}: op={op_name}")
            return op_name, resp
        print(f"[?] no op name in response from {model}: {json.dumps(resp)[:300]}", file=sys.stderr)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:500]
        print(f"[FAIL {e.code}] {model}: {err}", file=sys.stderr)
    except Exception as e:
        print(f"[ERR] {model}: {e}", file=sys.stderr)
    return None


def poll_until_done(op_name: str, model: str) -> dict:
    """Poll GET /operations/{name} until done. Veo jobs typically 60-300s."""
    base = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}"
    started = time.time()
    while True:
        resp = get_json(base)
        if resp.get("done"):
            elapsed = time.time() - started
            print(f"[DONE] {model} after {elapsed:.0f}s")
            return resp
        elapsed = time.time() - started
        print(f"  ...polling ({elapsed:.0f}s elapsed)")
        if elapsed > 900:  # 15 min cap
            raise TimeoutError("Veo job timeout")
        time.sleep(15)


def extract_video(resp: dict) -> bytes | None:
    """Get raw mp4 bytes from various possible response shapes."""
    # Format 1: response.generateVideoResponse.generatedSamples[0].video.uri
    response = resp.get("response", {})
    samples = (
        response.get("generateVideoResponse", {}).get("generatedSamples")
        or response.get("videos")
        or response.get("predictions", [{}])[0].get("videos")
        or []
    )
    if not samples and "predictions" in response:
        # Vertex-style: predictions[].bytesBase64Encoded
        preds = response.get("predictions", [])
        for p in preds:
            if "bytesBase64Encoded" in p:
                return base64.b64decode(p["bytesBase64Encoded"])
    for s in samples:
        # uri form
        video = s.get("video") or s
        uri = video.get("uri")
        if uri:
            sep = "&" if "?" in uri else "?"
            url = f"{uri}{sep}key={API_KEY}"
            print(f"  downloading {url[:120]}...")
            return download_bytes(url)
        # base64 form
        if "bytesBase64Encoded" in video:
            return base64.b64decode(video["bytesBase64Encoded"])
    return None


def main():
    print(f"hero image: {HERO_IMG} ({HERO_IMG.stat().st_size//1024} KB)")
    op_name = None
    used_model = None
    full_resp = None
    for model in MODELS_TO_TRY:
        result = try_kickoff(model)
        if result:
            op_name, full_resp = result
            used_model = model
            break
    if not op_name:
        print("\nALL MODELS FAILED. Likely API tier without Veo access.", file=sys.stderr)
        sys.exit(2)

    print(f"\nWaiting for video generation (typically 1-5 min)...")
    final = poll_until_done(op_name, used_model)

    if final.get("error"):
        print(f"ERROR in operation: {final['error']}", file=sys.stderr)
        sys.exit(3)

    video_bytes = extract_video(final)
    if not video_bytes:
        print(f"Could not extract video. Full response saved to /tmp/veo-resp.json", file=sys.stderr)
        Path("/tmp/veo-resp.json").write_text(json.dumps(final, indent=2)[:5000])
        sys.exit(4)

    OUT_MP4.parent.mkdir(parents=True, exist_ok=True)
    OUT_MP4.write_bytes(video_bytes)
    print(f"\n[SAVED] {OUT_MP4} ({len(video_bytes)//1024} KB)")


if __name__ == "__main__":
    main()
