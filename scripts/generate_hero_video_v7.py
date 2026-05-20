#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 v7 — "OSAKA STRATA HUSHED" 色調整版

v6 は構図が完璧だったが、右側の太陽が明るすぎてヒーロー上の text 視認性が
損なわれていた。v7 ではコンテンツ（淀川の鉄橋・工業倉庫・現代摩天楼の
3層）はそのまま、グレーディングだけを matte/hushed に振り直す。

調整方針:
  1. 直射日光は重い霧で diffuse  → blown-out highlight 排除
  2. 全体を一段暗めの cinematic palette に
  3. mid-tone を navy 寄せで text 上の読みやすさ確保
  4. ブランドカラー deep navy × brass gold への色寄せをさらに強化
  5. matte finish — 高コントラストを避け、目に優しいトーン

実行: python3 scripts/generate_hero_video_v7.py
出力: docs/assets/img/hero/hero-main.mp4 (v6 は hero-main-v6.mp4 へ退避)
"""
import json, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_KEY = (ROOT / ".env").read_text().split("=", 1)[1].strip()

MODELS = [
    "veo-3.1-generate-preview",
    "veo-3.0-generate-001",
    "veo-3.1-fast-generate-preview",
]

PROMPT = (
    "[STYLE] Award-winning Japanese civic infrastructure cinematography, "
    "moody and contemplative, in the tonal tradition of Roger Deakins' "
    "'Blade Runner 2049' or Hoyte van Hoytema's 'Tenet' night sequences "
    "applied to a daylight scene. Anamorphic 2.39:1 widescreen, single "
    "continuous take, slow contemplative pace. Subject: a working Japanese "
    "river at the very edge of dawn — heavy atmospheric haze, water heritage "
    "flowing through industrial-era warehouses to the contemporary skyline. "
    "Civic and wholesome subject matter: river, embankments, iron-truss "
    "bridge, warehouses, factory chimneys, distant glass skyline. "
    "No people, no vehicles, no machinery, no animals. "
    "\n\n"
    "[CAMERA] ARRI Alexa Mini LF with Cooke S7/i 32mm anamorphic prime lens, "
    "24fps, ProRes 4444 XQ. Rectilinear projection, flat undistorted FOV, "
    "absolutely no fisheye, no barrel distortion, no vignetting at frame edges, "
    "no circular dark corners. The camera viewpoint is the audience's eye — "
    "the aerial rig itself is NEVER visible in the frame. No drone, no "
    "quadcopter, no helicopter ever shown. Stable smooth vertical-rise motion, "
    "zero jitter, zero wobble. Single continuous take, no cuts. "
    "\n\n"
    "[GRADE — KEY CHANGES FROM v6]\n"
    "MATTE FINISH. Predominantly dark cinematic palette. Sky and overall "
    "scene biased toward DEEP NAVY #0F1B2D occupying the upper 60% of the "
    "frame. Brass gold #B8935E confined to a NARROW band along the horizon, "
    "subtle and contained — NOT a wide golden burst. "
    "ABSOLUTELY NO blown-out highlights. No overexposed sun. No bright lens "
    "flare bursts. Highlights gently rolled off — the brightest area should "
    "still hold visible texture and color. "
    "Mid-tones lifted toward cool navy-blue, not warm sepia. Shadows crushed "
    "to deep navy-black, preserving detail but kept moody. "
    "Heavy atmospheric haze and morning mist FILTERING the light throughout "
    "the entire frame — the sun is felt, not seen. Diffuse luminance "
    "(no point-source brightness). "
    "Subtly desaturated overall, but with a clear teal-orange spine. "
    "Very fine digital grain — extremely subtle. The intent: cinematic, "
    "hushed, atmospheric — and EASY ON THE EYES so that white serif text "
    "overlaid on this frame remains effortlessly legible. "
    "CRITICAL: the output frame must be a CLEAN modern digital cinema "
    "rendering. No film stock simulation in the image itself. "
    "No printed edge markings, no film perforation holes, no celluloid "
    "frame borders, no 'Kodak' text, no frame numbers like '0B8935E', "
    "no analog film artifacts BAKED INTO the image. The frame fills the "
    "ENTIRE 16:9 canvas edge-to-edge with no inner border."
    "\n\n"
    "[LIGHTING] Pre-dawn blue hour transitioning into VERY soft, diffuse "
    "first light. The sun has technically risen but is completely diffused "
    "by thick atmospheric haze — its position can only be inferred from a "
    "subtle warm gradient near the horizon. No direct sunbeams, no harsh "
    "shadows. Color temperature held at a cool 4800K throughout. "
    "Even, soft, ambient luminance. "
    "\n\n"
    "[0:00 - 0:02 OPENING — river surface] "
    "Viewpoint at 0.5m above calm river water. Foreground RIGHT: weathered "
    "concrete-and-stone embankment, vertical wall about 4m tall, decades "
    "of patina, moss, water marks. Foreground LEFT: open river water "
    "stretching to opposite bank, slow current, gentle reflections. "
    "Thick morning mist drifts LOW across the water surface. Background "
    "obscured by haze — no buildings yet. Viewpoint begins absolutely "
    "smooth vertical ascent at 0.4 m/s. The frame holds in a calm, "
    "near-monochromatic deep-navy + faint warm wash. "
    "\n\n"
    "[0:02 - 0:05 MIDDLE — bridge reveals through mist] "
    "Viewpoint rises 6m, very gradual tilt-down 8 degrees. Mist begins to "
    "thin REVEALING but not removing the haze. A massive iron-truss bridge "
    "spans the river — simple boxy iron truss, NO complex cable-stayed "
    "structure, NO suspension cables, just solid riveted iron beams in "
    "triangular truss pattern. Painted faded industrial gray-green with "
    "rust patina, color reads MUTED, not vivid. Beyond the bridge: low "
    "rectangular warehouse buildings with corrugated metal roofs (Showa-era "
    "industrial, utilitarian, NOT residential), brick factory chimneys with "
    "thin desaturated steam plumes. Still no buildings closer than 50m. "
    "\n\n"
    "[0:05 - 0:08 CLIMAX — three-layered cityscape, hushed] "
    "Viewpoint reaches high altitude with tilt-down at 30 degrees, holding "
    "altitude steady. Three temporal strata of the city visible in a single "
    "MUTED composition: "
    "FOREGROUND — weathered concrete-and-stone river embankment, soft "
    "ambient light catching wet stone subtly; "
    "MIDGROUND — Showa-era industrial warehouses with corrugated rooftops "
    "and brick smokestacks, all in muted tones; "
    "BACKGROUND — silhouettes of contemporary glass-and-steel high-rise "
    "office towers on the far horizon, almost merging with the haze. "
    "Sky fills the upper 60% of frame: deep navy #0F1B2D at top, "
    "transitioning to a NARROW brass-gold band #B8935E at the horizon. "
    "The transition should be gradual and contained. NO sun flare. "
    "Long, soft, diffuse shadows. The river winds away into haze toward "
    "the modern skyline — the visual metaphor of heritage flowing into "
    "future, executed in a HUSHED, READABLE tonal register. "
    "\n\n"
    "[NEGATIVE PROMPT] "
    "ABSOLUTELY NO blown-out highlights, no overexposed sun, no bright "
    "lens flare bursts, no harsh sunbeams, no direct sunlight rays, no "
    "harsh sun glare, no oversaturated golden hour, no neon-orange sky. "
    "ABSOLUTELY NO traditional Japanese wooden residential buildings — "
    "no machiya, no two-story wooden houses with kawara roofs in the "
    "foreground, no traditional residential architecture. "
    "ABSOLUTELY NO paper lanterns — no chouchin, no andon, no hanging lit "
    "lanterns of any color, no festival lanterns. "
    "ABSOLUTELY NO narrow residential alleyways, no Tobita Shinchi, no "
    "Hozenji Yokocho, no red-light district imagery. "
    "No people, no humans, no workers, no figures, no silhouettes, "
    "no animals, no birds, no insects. "
    "No vehicles, no cars, no trucks, no trains, no boats on the river. "
    "No machinery, no construction equipment, no cranes, no excavators. "
    "No flying objects: no drones, no quadcopters, no UAVs, no helicopters, "
    "no aircraft, no balloons, no kites. The camera rig itself must "
    "NEVER appear in the shot. "
    "No fisheye distortion, no GoPro action camera look, no barrel "
    "distortion, no pincushion distortion, no curved horizons, "
    "no circular vignetting, no dark circular frame edges, no porthole "
    "effect. Rectilinear lens projection only. "
    "No broken glass artifacts, no chromatic aberration ghosting. "
    "No readable text, no readable kanji, no readable katakana, no English "
    "text, no logos, no brand markings. "
    "No specific landmark buildings — no Tsutenkaku tower, no Tower of the "
    "Sun, no Osaka Castle, no Umeda Sky Building. "
    "No high contrast lighting. No vivid saturated colors. No HDR look. "
    "No flat color blocks in sky — only smooth gradients. "
    "No CGI plastic look. No cartoon look. No anime style. "
    "NO FILM STOCK SIMULATION. No printed film edge markings inside the "
    "frame. No frame numbers (like '0B8935E', '4B8935E'). "
    "No celluloid perforation holes. No film border around the image. "
    "No analog film overlay graphics. No 'shot on film' Polaroid frame. "
    "No vintage film texture overlay. No light leaks burned into the image. "
    "The output must be a clean modern digital rendering, edge-to-edge, "
    "with no internal frame or border whatsoever. "
    "Photoreal MUTED cinematography only. Sharp focus throughout the "
    "shot subjects but with heavy atmospheric haze softening the air. "
    "Permitted architecture only: weathered concrete river embankments, "
    "iron truss bridges with simple riveted construction, Showa-era "
    "industrial warehouses with corrugated metal roofs, brick factory "
    "chimneys with thin steam plumes, and distant modern glass-curtain "
    "high-rise silhouettes on the horizon — all in MUTED tones."
)

OUT = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main.mp4"
BACKUP = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main-v6.mp4"


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
    if OUT.exists():
        OUT.rename(BACKUP)
        print(f"[BACKUP] hero-main.mp4 (v6) → {BACKUP.name}")

    op, used = None, None
    for m in MODELS:
        op, err = kickoff(m)
        if op:
            used = m
            print(f"[OK] kicked off with {m}")
            break
        print(f"[FAIL] {m}: {err}", file=sys.stderr)
    if not op:
        if BACKUP.exists():
            BACKUP.rename(OUT)
        sys.exit("All Veo variants failed")

    print(f"\nWaiting for Veo to render...")
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
        if BACKUP.exists():
            BACKUP.rename(OUT)
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
