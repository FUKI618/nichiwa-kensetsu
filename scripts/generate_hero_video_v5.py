#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 v5 — "OSAKA STRATA — 街の地層"

コンセプト: 大阪の「時間の重層性」を1テイクで視覚化。
下町（昭和木造密集）→ 中層商業ビル → 摩天楼シルエット の3レイヤーが同フレームに重なる。
人物・機械ゼロ。実在固有ランドマーク（通天閣・太陽の塔等）は名指しせず、
特徴的形状で「大阪らしさ」を出す。

実行: /Users/fuki/.scrapling-venv/bin/python3 scripts/generate_hero_video_v5.py
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
]

PROMPT = (
    "[STYLE] Award-winning Japanese urban cinematography in the style of "
    "Wim Wenders' 'Tokyo-ga' meets Christopher Doyle's '2046', anamorphic 2.39:1 widescreen, "
    "single continuous take, contemplative long-shot. Theme: layered stratification "
    "of an Osaka neighborhood — old wooden lowtown in the foreground, mid-century "
    "concrete buildings in the midground, contemporary high-rise silhouettes on the horizon. "
    "No people anywhere. No vehicles. No machinery. No animals. "
    "\n\n"
    "[CAMERA] Shot on ARRI Alexa Mini LF with Cooke S7/i 32mm anamorphic prime lens, 24fps, "
    "ProRes 4444 XQ, very subtle horizontal anamorphic lens flares from low sun. "
    "Rectilinear projection, flat undistorted field of view, no fisheye, no barrel distortion, "
    "no vignetting at frame edges, no circular dark corners. "
    "Camera held by a stabilized aerial cinematography rig — but the rig itself is NEVER visible "
    "in the frame. The viewer is looking THROUGH the camera, never at it. "
    "Absolutely stable smooth vertical-rise take, zero jitter, zero wobble. "
    "Single continuous take, no cuts, no transitions. "
    "\n\n"
    "[GRADE] Subtly desaturated teal-orange grade preserving deep shadows. "
    "Sky transitions across the frame from deep navy #0F1B2D at top "
    "to warm brass gold #B8935E near horizon. Fine 35mm film grain "
    "emulating Kodak Vision3 250D daylight stock. Slight halation on highlights. "
    "\n\n"
    "[LIGHTING] Early morning blue hour transitioning into first golden hour light. "
    "Color temperature warming from 4500K to 3800K over the 8-second shot. "
    "Low-angle warm key light entering from screen-right at 4-degree elevation, "
    "creating long horizontal shadows extending screen-left. Light atmospheric haze. "
    "Faint amber lantern and shopfront glow in the lowtown foreground (still on from night). "
    "\n\n"
    "[0:00 - 0:02 OPENING — Ultra-low alley level] "
    "The camera viewpoint starts at 1 meter above damp asphalt in a narrow Showa-era Japanese lowtown alley. "
    "Foreground: weathered wooden two-story machiya-style buildings with kawara clay tile roofs, "
    "tangled overhead electrical wires, faded paper lanterns (chouchin) glowing soft amber, "
    "shuttered storefronts, narrow alleyway perspective. Light morning mist drifting at ankle level. "
    "Background is completely obscured by mist and lowtown rooflines. "
    "The viewpoint begins absolutely smooth vertical ascent at 0.4 m/s, "
    "no horizontal drift, no panning. Sky visible above is clean — no flying objects, no birds, "
    "no aircraft, no drones, no UAVs, no helicopters, no kites, no balloons in the frame. "
    "\n\n"
    "[0:02 - 0:05 MIDDLE — Rising through the strata] "
    "Drone continues vertical rise, gaining 6 more meters of altitude. "
    "Tilt down 10 degrees gradually. The lowtown roofs spread out below. "
    "Now visible in the midground: a layer of 1960s-1980s mid-rise concrete-and-tile commercial "
    "buildings (4-8 stories tall), boxy Showa modernist architecture, rooftop water tanks, "
    "vintage neon-sign frames (no readable characters), exterior air-conditioning units, "
    "fire escape ladders. Sun beginning to crest behind the buildings off-screen right. "
    "Atmospheric haze remains in the middle distance. "
    "\n\n"
    "[0:05 - 0:08 CLIMAX — Three-strata reveal] "
    "Drone reaches high altitude with tilt-down at 35 degrees, holding altitude steady. "
    "All three layers now visible in a single composition: "
    "FOREGROUND — the cluster of low Showa-era wooden machiya rooftops the shot started in; "
    "MIDGROUND — the band of mid-century concrete commercial buildings; "
    "BACKGROUND — the distant silhouettes of contemporary glass-and-steel high-rise towers "
    "(generic modern Japanese skyscrapers, no recognizable specific buildings, "
    "no observation tower with a circular crown, no Tutankhamun-shaped landmark sculpture). "
    "Sky fills the upper half of the frame, transitioning smoothly from deep navy #0F1B2D "
    "at the very top to warm brass gold #B8935E along the horizon. "
    "Subtle horizontal anamorphic lens flare streaking across the frame from screen-right. "
    "Power lines and utility poles cast long shadows. Final shot composition strongly emphasizes "
    "the temporal layering — old, middle, new — all coexisting in a single Japanese urban frame. "
    "\n\n"
    "[NEGATIVE PROMPT] "
    "No people, no humans, no workers, no figures, no silhouettes of people, no animals, no birds, no insects. "
    "No vehicles, no cars, no trucks, no trains, no boats. "
    "No machinery, no construction equipment, no cranes, no excavators. "
    "No flying objects in frame: no drones, no quadcopters, no UAVs, no helicopters, no aircraft, "
    "no airplanes, no balloons, no kites, no birds, no flying debris. The camera rig itself must "
    "NEVER appear in the shot — the viewer looks through the lens, never sees the lens. "
    "No fisheye distortion, no GoPro action camera look, no barrel distortion, no pincushion distortion, "
    "no curved horizons, no curved verticals, no circular vignetting, no dark circular frame edges, "
    "no porthole effect, no spherical projection. Rectilinear lens projection only. "
    "No broken glass artifacts at frame corners, no chromatic aberration ghosting, "
    "no shattered-glass texture at frame edges, no cracked-lens overlay, no dirty lens overlay. "
    "No readable text, no readable kanji characters, no readable katakana, no English text, "
    "no logos, no brand markings, no shop names, no advertising. "
    "No specific landmark buildings — no Tsutenkaku tower, no observation tower with circular crown, "
    "no Tower of the Sun, no Osaka Castle, no specific recognizable architecture. "
    "No torii gates. No temples. No shrines. No castles. "
    "No warping or distortion of building geometry. No melting roofs, no impossible perspectives. "
    "No double-exposure or ghosting artifacts. No flat color blocks in sky (must be smooth gradient). "
    "No CGI plastic look. No cartoon look. No anime style. Photoreal cinematography only. "
    "No motion blur on buildings or background. Sharp focus throughout. "
    "Accurate Japanese suburban / lowtown architecture only — "
    "real kawara clay tile roofs, real Showa-era wooden two-story machiya houses, "
    "real 1960s-1980s mid-rise concrete commercial buildings, "
    "real modern glass-curtain high-rise silhouettes in the distance."
)

OUT = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main.mp4"
OUT_BACKUP = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main-v4.mp4"


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
    # Backup previous hero
    if OUT.exists():
        OUT.rename(OUT_BACKUP)
        print(f"[BACKUP] {OUT.name} → {OUT_BACKUP.name}")

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
        # Restore backup
        if OUT_BACKUP.exists():
            OUT_BACKUP.rename(OUT)
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
        # Restore backup
        if OUT_BACKUP.exists():
            OUT_BACKUP.rename(OUT)
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
