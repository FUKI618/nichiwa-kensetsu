#!/usr/bin/env python3
"""
代表者の顔写真を実ブラウザ経由で取得する。
直リンクは as.okmart.info の CDN/Cloudflare に弾かれるため、
nichiwa-kensetu.com の代表挨拶ページを開いた状態でスクリーンショットして
顔写真の領域だけクロップする。

実行: /Users/fuki/.scrapling-venv/bin/python3 scripts/fetch_ceo_photo.py
出力: docs/assets/img/people/ceo-yoshida.jpg
"""
from playwright.sync_api import sync_playwright
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "img" / "people" / "ceo-yoshida.jpg"
OUT.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(
        viewport={'width': 1280, 'height': 1800},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    )
    page = ctx.new_page()
    page.goto('https://nichiwa-kensetu.com/representative/', wait_until='domcontentloaded')
    page.wait_for_timeout(3500)

    # Force lazy-load
    page.evaluate("""() => {
        window.scrollTo(0, document.body.scrollHeight);
    }""")
    page.wait_for_timeout(2000)
    page.evaluate("() => window.scrollTo(0, 0)")
    page.wait_for_timeout(1500)

    # Locate the CEO portrait — large img not the logo
    handle = page.query_selector("img.wp-image-282, img[src*='C2348838']")
    if handle is None:
        # fallback: largest img in main content
        handle = page.query_selector("main img:not(.custom-logo)")

    if handle:
        # Element screenshot — captures the rendered image even if cross-origin
        handle.screenshot(path=str(OUT), type='jpeg', quality=92)
        print(f"[OK] saved {OUT}")
        # Check size
        size = OUT.stat().st_size
        print(f"     size: {size} bytes")
    else:
        print("[FAIL] CEO image element not found")

    browser.close()
