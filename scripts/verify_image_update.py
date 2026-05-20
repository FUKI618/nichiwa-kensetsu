#!/usr/bin/env python3
"""画像差し替え + ナビ統合の視認検証 (1440px desktop + 390px mobile)"""
from playwright.sync_api import sync_playwright
import time

OUT = "/Users/fuki/Code/LP作成/日和建設/screenshots"
BASE = "http://localhost:8989/nichiwa-kensetsu"
PAGES = [
    ("home", "/"),
    ("company", "/company/"),
    ("services", "/services/"),
    ("strengths", "/strengths/"),
    ("sustainability", "/sustainability/"),
    ("contact", "/contact.html"),
]
SIZES = [("desktop-1440", 1440, 900), ("mobile-390", 390, 844)]

results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for label, w, h in SIZES:
        ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, reduced_motion="reduce")
        for name, path in PAGES:
            page = ctx.new_page()
            page.goto(f"{BASE}{path}?t={int(time.time())}", wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(1500)
            page.evaluate("() => document.querySelectorAll('video').forEach(v=>v.remove())")
            page.evaluate("""() => new Promise(r => {
              let y=0; const i=setInterval(()=>{ y+=600; window.scrollTo(0,y);
                if(y>=document.body.scrollHeight){clearInterval(i); window.scrollTo(0,0); r();}}, 60);})""")
            page.wait_for_timeout(1000)
            page.screenshot(path=f"{OUT}/verify-{name}-{label}.png", full_page=True, timeout=30000)
            broken = page.evaluate("() => Array.from(document.images).filter(i=>i.complete && i.naturalWidth===0).map(i=>i.src)")
            nav_items = page.evaluate("() => Array.from(document.querySelectorAll('.global-nav a')).map(a=>a.textContent.trim())")
            results.append((name, label, broken, nav_items))
            page.close()
        ctx.close()
    browser.close()

for name, label, broken, nav in results:
    print(f"[{label}] {name}: brokenImg={len(broken)} nav={nav}")
    if broken:
        for b in broken:
            print(f"    BROKEN: {b}")
