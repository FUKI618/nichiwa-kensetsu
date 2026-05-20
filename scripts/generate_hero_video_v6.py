#!/usr/bin/env python3
"""
日和建設 ヒーロー動画 v6 — "MORNING ON THE YODO — 淀川の朝"

v5.1の問題: 「狭い路地+木造machiya+提灯」の3要素が揃い、
学習データ上「飛田新地（風俗街）」を強く参照する映像になってしまった。

v6 の対策: 水都・公共インフラ・産業遺産 へ完全シフト。
- machiya → 石垣堤防・倉庫
- 提灯   → 橋桁・煙突
- 路地   → 川面・河岸
の3点置換で、Tobita Shinchi アソシエーションを物理的に排除。

実行: python3 scripts/generate_hero_video_v6.py
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
    "[STYLE] Award-winning Japanese civic infrastructure cinematography "
    "in the documentary tradition of Wim Wenders' 'Tokyo-ga' and "
    "Naomi Kawase's contemplative river scenes. Anamorphic 2.39:1 widescreen, "
    "single continuous take, contemplative long-shot. "
    "Theme: a working Japanese river at dawn — water heritage flowing through "
    "industrial-era warehouses to the contemporary skyline. "
    "Subject matter is CIVIC and WHOLESOME: river, embankments, bridge, warehouses, "
    "factory chimneys, distant glass skyline. "
    "Absolutely NO traditional residential machiya buildings, NO hanging paper lanterns "
    "of any color, NO narrow residential alleyways, NO entertainment district aesthetic. "
    "No people anywhere. No vehicles. No machinery. No animals. No birds. "
    "\n\n"
    "[CAMERA] Shot on ARRI Alexa Mini LF with Cooke S7/i 32mm anamorphic prime lens, 24fps, "
    "ProRes 4444 XQ, very subtle horizontal anamorphic lens flares from low sun. "
    "Rectilinear projection, flat undistorted field of view, NO fisheye, NO barrel distortion, "
    "NO vignetting at frame edges, NO circular dark corners. "
    "The camera viewpoint is the audience's eye. The aerial rig itself is NEVER visible "
    "in the frame. No drone, no quadcopter, no helicopter ever shown. "
    "Absolutely stable smooth vertical-rise motion, zero jitter, zero wobble. "
    "Single continuous take, no cuts, no transitions. "
    "\n\n"
    "[GRADE] Subtly desaturated teal-orange grade preserving deep shadows. "
    "Sky transitions across the frame from deep navy #0F1B2D at top "
    "to warm brass gold #B8935E near horizon. Fine 35mm film grain "
    "emulating Kodak Vision3 250D daylight stock. Slight halation on highlights. "
    "\n\n"
    "[LIGHTING] Pre-dawn blue hour transitioning into first golden hour. "
    "Color temperature warming from 4500K to 3800K over the 8-second shot. "
    "Low warm key light from screen-right at 4-degree elevation, "
    "creating long horizontal shadows extending screen-left. "
    "Light atmospheric river haze drifting horizontally. "
    "NO amber glow at street level. NO lit lanterns. NO neon signs. "
    "Only natural pre-dawn ambient blue + first sunlight from the horizon. "
    "\n\n"
    "[0:00 - 0:02 OPENING — river surface] "
    "The camera viewpoint starts at 0.5 meter above the calm surface of a wide "
    "Japanese urban river. Foreground RIGHT: a weathered concrete-and-stone "
    "river embankment, vertical wall about 4 meters tall, showing decades of patina, "
    "moss, water marks, occasional drainage pipes. Foreground LEFT: open river water "
    "stretching to the opposite bank, slow current, gentle reflections of pre-dawn "
    "sky on water. Thin morning mist drifting low over the water surface. "
    "Background is obscured by mist — no buildings visible yet. "
    "ABSOLUTELY NO machiya, NO lanterns, NO alleys. Just water, stone embankment, mist. "
    "The viewpoint begins absolutely smooth vertical ascent at 0.4 m/s. "
    "\n\n"
    "[0:02 - 0:05 MIDDLE — bridge reveals through mist] "
    "Viewpoint rises 6 more meters of altitude, very gradual tilt-down 8 degrees. "
    "The mist begins to thin. A massive steel-truss bridge spans the river — "
    "simple boxy iron truss construction, NO complex cable-stayed structure, "
    "NO suspension cables, just solid riveted iron beams in a triangular truss pattern. "
    "The bridge is painted faded industrial gray-green with rust patina. "
    "Beyond the bridge, midground SHAPES begin to emerge through the haze: "
    "low rectangular warehouse buildings with corrugated metal roofs (Showa-era "
    "industrial architecture, 2-3 stories, completely utilitarian, NOT residential), "
    "and a few brick factory chimneys with thin white steam plumes rising. "
    "Still no buildings closer than 50 meters from camera. "
    "\n\n"
    "[0:05 - 0:08 CLIMAX — three-layered cityscape] "
    "Viewpoint reaches high altitude with tilt-down at 30 degrees, holding altitude steady. "
    "All three temporal strata of the city now visible in a single composition: "
    "FOREGROUND — the weathered concrete-and-stone river embankment continues "
    "into the frame, sun catching the wet stone surface; "
    "MIDGROUND — a band of Showa-era industrial warehouses with corrugated rooftops "
    "and brick smokestacks lines the riverbank, sun catching the rusty rooftops; "
    "BACKGROUND — silhouettes of contemporary glass-and-steel high-rise office towers "
    "on the far horizon (generic modern Japanese skyscrapers, no specific recognizable "
    "buildings). Sky fills the upper half: deep navy #0F1B2D at top transitioning "
    "smoothly to warm brass gold #B8935E along the horizon. "
    "Subtle horizontal anamorphic lens flare from screen-right. "
    "Long horizontal shadows from warehouses extending across the river surface. "
    "The river itself winds away into the distance toward the modern skyline — "
    "the visual metaphor of heritage flowing into future. "
    "\n\n"
    "[NEGATIVE PROMPT] "
    "ABSOLUTELY NO traditional Japanese wooden residential buildings — no machiya, "
    "no two-story wooden houses with kawara roofs in the foreground, no shopfront "
    "wooden facades, no traditional residential architecture of any kind. "
    "ABSOLUTELY NO paper lanterns — no chouchin, no andon, no hanging lit lanterns "
    "of any color (no amber, no red, no white), no festival lanterns. "
    "ABSOLUTELY NO narrow residential alleyways — no tight streets with houses on "
    "both sides, no entertainment district streets, no izakaya streets, "
    "no Tobita Shinchi, no Hozenji Yokocho, no Hoppy Street, no red-light district imagery. "
    "ABSOLUTELY NO entertainment district visual cues whatsoever. "
    "No people, no humans, no workers, no figures, no silhouettes, no animals, no birds, no insects. "
    "No vehicles, no cars, no trucks, no trains, no boats on the river. "
    "No machinery, no construction equipment, no cranes, no excavators. "
    "No flying objects: no drones, no quadcopters, no UAVs, no helicopters, no aircraft, "
    "no balloons, no kites. The camera rig itself must NEVER appear in the shot. "
    "No fisheye distortion, no GoPro action camera look, no barrel distortion, "
    "no pincushion distortion, no curved horizons, no circular vignetting, "
    "no dark circular frame edges, no porthole effect. Rectilinear lens projection only. "
    "No broken glass artifacts, no chromatic aberration ghosting, "
    "no shattered-glass texture at frame edges, no dirty lens overlay. "
    "No readable text, no readable kanji, no readable katakana, no English text, "
    "no logos, no brand markings, no shop names, no advertising signs, no neon. "
    "No specific landmark buildings — no Tsutenkaku tower, no Tower of the Sun, "
    "no Osaka Castle, no Umeda Sky Building, no recognizable Osaka landmarks. "
    "No torii gates, no temples, no shrines, no castles. "
    "No warping of building geometry. No melting roofs, no impossible perspectives. "
    "No double-exposure or ghosting artifacts. No flat color blocks in sky (smooth gradient only). "
    "No CGI plastic look. No cartoon look. No anime style. Photoreal cinematography only. "
    "Sharp focus throughout. "
    "Permitted architecture only: weathered concrete river embankments with patina, "
    "iron truss bridges with simple riveted construction, "
    "Showa-era industrial warehouses with corrugated metal roofs (utilitarian, NOT residential), "
    "brick factory chimneys with thin steam plumes, "
    "and distant modern glass-curtain high-rise silhouettes on the horizon."
)

OUT = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main.mp4"
BACKUP_V5 = ROOT / "docs" / "assets" / "img" / "hero" / "hero-main-v5_1.mp4"


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
        # Move v5.1 to backup
        OUT.rename(BACKUP_V5)
        print(f"[BACKUP] hero-main.mp4 (v5.1) → {BACKUP_V5.name}")

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
        if BACKUP_V5.exists():
            BACKUP_V5.rename(OUT)
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
        if BACKUP_V5.exists():
            BACKUP_V5.rename(OUT)
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
