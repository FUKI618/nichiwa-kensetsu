#!/usr/bin/env python3
"""
日和建設 LP - AI画像生成スクリプト
Gemini API (gemini-2.5-flash-image) でフォトリアル画像を17枚生成。

メモリ準拠:
- "AI画像生成にテキストを入れない": プロンプトに no text/no logos/no readable signs を多重指定
- 生成後の目視確認はユーザー側で実施する

実行: GEMINI_API_KEY=<key> python3 scripts/generate_images.py
"""
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip()
                break

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found", file=sys.stderr)
    sys.exit(1)

MODEL = "gemini-2.5-flash-image"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

ROOT = Path(__file__).resolve().parents[1] / "制作物" / "assets" / "img"

COMMON_SUFFIX = (
    " cinematic lighting, photorealistic, ultra-detailed, shot on 35mm,"
    " shallow depth of field, dust particles in the air,"
    " no text, no logos, no watermarks, no signage with letters,"
    " no readable signs, no kanji on walls, no labels, no name tags."
)

JOBS = [
    # (path_relative_to_assets_img, prompt, aspect_hint)
    ("hero/hero-01.png",
     "Wide cinematic shot of a Japanese demolition site at golden hour. "
     "A partially demolished two-story wooden house in the foreground, "
     "yellow long-arm excavator carefully reaching into the structure, "
     "crew of three Japanese workers in white helmets and navy work jackets, "
     "dust softly drifting in warm sunlight, surrounding scaffolding with green safety nets, "
     "moody dark navy sky transitioning to amber, strong sense of dignity and respect for the building. "
     "Aspect ratio 16:9.",
     "16:9"),

    ("services/demolition.png",
     "Close-up of a Japanese demolition foreman's hands holding a clipboard "
     "on a demolition site, wearing white safety helmet and gloves. "
     "RC building partially demolished in soft background bokeh, "
     "warm late-afternoon light, sense of meticulous planning. "
     "Aspect ratio 4:5 portrait.",
     "4:5"),

    ("services/asbestos.png",
     "A Japanese abatement worker in full white protective suit and hood, "
     "industrial respirator mask, inside a sealed negative-pressure "
     "containment area with translucent plastic sheeting all around, "
     "a plain blue industrial blower visible softly in the background, "
     "eerie cool-blue tone with one warm work light, sense of careful protocol. "
     "All equipment surfaces are completely blank, with absolutely no labels, "
     "no logos, no text, no stickers, no signage. "
     "Aspect ratio 4:5 portrait.",
     "4:5"),

    ("services/coating.png",
     "A Japanese painter in navy work uniform applying topcoat with a roller "
     "to a beige exterior wall of a low-rise commercial building, "
     "scaffolding with safety net softly in the frame, late morning light, "
     "crisp shadow lines, sense of craftsmanship and steady hand. "
     "Aspect ratio 4:5 portrait.",
     "4:5"),

    ("reasons/supervisor.png",
     "Portrait of a Japanese male site supervisor in his late 40s, "
     "white safety helmet, navy work jacket. "
     "Standing slightly off-center in front of a softly blurred construction site, "
     "calm confident expression, soft window light from camera left, "
     "shot on 85mm f/1.4, shallow depth of field. "
     "Aspect ratio 4:5 portrait.",
     "4:5"),

    ("works/work-01.png",
     "Wide shot of a small two-story wooden Japanese cultural housing "
     "mid-demolition, mini excavator gently picking apart the second floor, "
     "dust softly visible, residential neighborhood backdrop, "
     "overcast diffuse light. Aspect ratio 4:3.",
     "4:3"),

    ("works/work-02.png",
     "A six-story reinforced concrete building partially demolished "
     "in central Osaka, large excavator with long arm and crusher attachment, "
     "green safety netting on remaining floors, late afternoon light. "
     "Aspect ratio 4:3.",
     "4:3"),

    ("works/work-03.png",
     "Aerial-level view of a warehouse with corrugated slate roofing "
     "covered by full containment sheeting and scaffolding, "
     "two workers in white protective suits on the roof carefully removing slate panels, "
     "overcast soft light. Aspect ratio 4:3.",
     "4:3"),

    ("works/work-04.png",
     "Steel-frame factory building being dismantled, "
     "exposed I-beams, oxy-acetylene cutting sparks against dark interior, "
     "Japanese worker in navy fire-resistant gear, dramatic chiaroscuro lighting. "
     "Aspect ratio 4:3.",
     "4:3"),

    ("works/work-05.png",
     "Close-up of a gloved hand applying fresh sealant to an exterior wall "
     "expansion joint of a commercial building, scaffolding behind, "
     "crisp morning light, sense of precision craftsmanship. "
     "Aspect ratio 4:3.",
     "4:3"),

    ("works/work-06.png",
     "Small residential lot after partial demolition, freshly graded "
     "crushed stone surface, low garden walls remaining at edges, "
     "quiet residential street in background, soft afternoon light. "
     "Aspect ratio 4:3.",
     "4:3"),

    ("voices/voice-01.png",
     "Cinematic portrait of a Japanese man in his 60s wearing a beige cardigan "
     "over a collared shirt, gentle smile, sitting in a softly lit traditional "
     "Japanese living room with shoji screen background, warm window light, "
     "shallow depth of field. Aspect ratio 3:4 portrait.",
     "3:4"),

    ("voices/voice-02.png",
     "Cinematic portrait of a Japanese man in his 40s in a charcoal suit "
     "without tie, in a modern office with floor-to-ceiling windows blurred, "
     "calm confident expression, natural cool daylight. "
     "Aspect ratio 3:4 portrait.",
     "3:4"),

    ("voices/voice-03.png",
     "Cinematic portrait of a Japanese woman in her 40s wearing a soft "
     "beige sweater, standing in front of a freshly leveled empty lot "
     "where a house used to be, hopeful expression, golden hour light. "
     "Aspect ratio 3:4 portrait.",
     "3:4"),

    ("company/permit.png",
     "Top-down macro of a single sheet of premium Japanese washi paper "
     "with subtle fiber texture, a dark navy fountain pen resting diagonally, "
     "warm desk lamp light from upper right, very shallow depth of field. "
     "The paper has elegant blank space with no characters at all. "
     "Aspect ratio 4:5 portrait.",
     "4:5"),

    ("cta/cta-bg.png",
     "Wide cinematic shot of a Japanese site foreman from behind, "
     "white helmet and navy work jacket, looking out over a freshly cleared "
     "demolition site at dusk, silhouette against deep navy and amber sky, "
     "dust softly catching the last light, sense of completion and quiet pride. "
     "Aspect ratio 21:9 ultrawide.",
     "21:9"),

    ("hero/hero-02.png",
     "A Japanese demolition supervisor in clean navy work jacket and white helmet, "
     "politely bowing while handing a small gift box to an elderly neighbor "
     "at her front door, warm afternoon light in a quiet residential street, "
     "sense of sincerity. Aspect ratio 16:9.",
     "16:9"),
]


def call_api(prompt: str) -> bytes:
    body = {
        "contents": [{
            "parts": [{"text": prompt + COMMON_SUFFIX}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "16:9"},
        },
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    parts = payload.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        inline = p.get("inlineData") or p.get("inline_data")
        if inline and "data" in inline:
            return base64.b64decode(inline["data"])
    raise RuntimeError(f"No image in response: {json.dumps(payload)[:600]}")


def main():
    total = len(JOBS)
    failed = []
    for i, (rel, prompt, aspect) in enumerate(JOBS, 1):
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and out.stat().st_size > 5000:
            print(f"[{i:02d}/{total}] SKIP (exists): {rel}")
            continue
        # aspect-aware body
        body = {
            "contents": [{"parts": [{"text": prompt + COMMON_SUFFIX}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": aspect},
            },
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            ENDPOINT, data=data, headers={"Content-Type": "application/json"}
        )
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            parts = payload.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            img_bytes = None
            for p in parts:
                inline = p.get("inlineData") or p.get("inline_data")
                if inline and "data" in inline:
                    img_bytes = base64.b64decode(inline["data"])
                    break
            if not img_bytes:
                raise RuntimeError(f"no image: {json.dumps(payload)[:400]}")
            out.write_bytes(img_bytes)
            print(f"[{i:02d}/{total}] OK ({len(img_bytes)//1024}KB, {time.time()-t0:.1f}s, {aspect}): {rel}")
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")[:600]
            print(f"[{i:02d}/{total}] HTTP {e.code} on {rel}: {err}", file=sys.stderr)
            failed.append((rel, f"HTTP {e.code}: {err}"))
        except Exception as e:
            print(f"[{i:02d}/{total}] ERR on {rel}: {e}", file=sys.stderr)
            failed.append((rel, str(e)))
        time.sleep(1.0)
    if failed:
        print(f"\n{len(failed)} failed:")
        for rel, msg in failed:
            print(f"  - {rel}: {msg[:120]}")
        sys.exit(2)
    print("\nAll images generated.")


if __name__ == "__main__":
    main()
