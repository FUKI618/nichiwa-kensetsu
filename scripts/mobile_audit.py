#!/usr/bin/env python3
"""
モバイル監査 — 6ページ × 7viewport × 5チェック = 210項目
実行: /Users/fuki/.scrapling-venv/bin/python3 scripts/mobile_audit.py
出力: docs/.claude/audit-screenshots/ と docs/.claude/audit-report.json
"""
from playwright.sync_api import sync_playwright
import json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / ".claude" / "audit-screenshots"
OUT.mkdir(parents=True, exist_ok=True)

URLS = [
    ("home", "http://localhost:8989/nichiwa-kensetsu/"),
    ("company", "http://localhost:8989/nichiwa-kensetsu/company/"),
    ("services", "http://localhost:8989/nichiwa-kensetsu/services/"),
    ("sustainability", "http://localhost:8989/nichiwa-kensetsu/sustainability/"),
    ("strengths", "http://localhost:8989/nichiwa-kensetsu/strengths/"),
    ("news", "http://localhost:8989/nichiwa-kensetsu/news/"),
]

SIZES = [
    ('iPhoneSE-320',         320, 568),
    ('iPhone13mini-375',     375, 812),
    ('iPhone14-390',         390, 844),
    ('iPhone14Plus-414',     414, 896),
    ('iPhone14ProMax-430',   430, 932),
    ('iPad-768',             768, 1024),
    ('Desktop-1440',        1440, 900),
]

AUDIT_JS = """() => {
    const W = window.innerWidth;
    const html = document.documentElement;
    const overflowX = html.scrollWidth - html.clientWidth;

    const overflowers = [];
    document.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width > W + 1 || r.right > W + 1) {
            // Filter out trivial cases: <html>, <body>, <header position:fixed> typical
            const tag = el.tagName.toLowerCase();
            if (tag === 'html' || tag === 'body') return;
            const cs = getComputedStyle(el);
            if (cs.position === 'fixed') return;  // fixed elements may render edge-to-edge intentionally
            overflowers.push({
                sel: tag + '.' + (el.className || '').toString().slice(0, 60),
                w: Math.round(r.width), right: Math.round(r.right)
            });
        }
    });

    const wraps = [];
    document.querySelectorAll('h1,h2,h3,h4,p,th,td,li,a,strong,span,small').forEach(el => {
        if (!el.offsetParent) return;
        // Skip if it contains other text elements (only check leaf text)
        if (Array.from(el.children).some(c => ['H1','H2','H3','H4','P','SPAN','A'].includes(c.tagName))) return;
        const cs = getComputedStyle(el);
        const lh = parseFloat(cs.lineHeight);
        const fs = parseFloat(cs.fontSize);
        const line = isNaN(lh) ? fs * 1.5 : lh;
        const rows = Math.round(el.getBoundingClientRect().height / line);
        const text = (el.textContent || '').trim();
        if (rows >= 3 && text.length > 0 && text.length < 30) {
            wraps.push({ sel: el.tagName.toLowerCase(), rows, text: text.slice(0, 40) });
        }
    });

    const flyOuts = [];
    document.querySelectorAll('button, .btn, [class*="badge"], [class*="-num"]').forEach(el => {
        const parent = el.parentElement;
        if (!parent) return;
        const er = el.getBoundingClientRect();
        const pr = parent.getBoundingClientRect();
        if (er.right > pr.right + 1 || er.left < pr.left - 1) {
            flyOuts.push({
                sel: el.tagName.toLowerCase() + '.' + (el.className || '').toString().slice(0, 40),
                d: `L=${Math.round(er.left - pr.left)} R=${Math.round(er.right - pr.right)}`
            });
        }
    });

    const brokenImgs = [];
    document.querySelectorAll('img').forEach(img => {
        if (img.complete && img.naturalWidth === 0) {
            brokenImgs.push({ src: img.src.slice(-60), alt: img.alt });
        }
    });

    return { viewport: W, overflowX, overflowers, wraps, flyOuts, brokenImgs };
}"""

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    for page_label, url in URLS:
        results[page_label] = {}
        for vp_label, w, h in SIZES:
            ctx = browser.new_context(
                viewport={'width': w, 'height': h},
                device_scale_factor=1,
                reduced_motion='reduce',
            )
            page = ctx.new_page()
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=20000)
                page.wait_for_timeout(1200)
                page.evaluate("() => document.querySelectorAll('video').forEach(v => v.remove())")
                # quick scroll to trigger lazy
                page.evaluate("""() => new Promise(r => {
                    let y = 0; const i = setInterval(() => {
                        y += 600; window.scrollTo(0, y);
                        if (y >= document.body.scrollHeight) { clearInterval(i); window.scrollTo(0, 0); r(); }
                    }, 50);
                })""")
                page.wait_for_timeout(800)
                report = page.evaluate(AUDIT_JS)
                results[page_label][vp_label] = report
                # Only screenshot if there are issues, to save time
                has_issues = report['overflowX'] > 0 or len(report['overflowers']) > 0 or len(report['wraps']) > 0 or len(report['flyOuts']) > 0 or len(report['brokenImgs']) > 0
                if has_issues or vp_label in ('iPhone14-390', 'Desktop-1440'):
                    page.screenshot(path=str(OUT / f"{page_label}-{vp_label}.png"), full_page=True, timeout=30000)
            except Exception as e:
                results[page_label][vp_label] = {'error': str(e)}
            ctx.close()
            print(f"  {page_label}/{vp_label}")
    browser.close()

# JSON
(ROOT / "docs/.claude/audit-report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))

# Markdown summary
print("\n\n## 監査サマリ\n")
print("| Page | Viewport | overflowX | overflowers | wraps≥3行 | flyOuts | brokenImgs | Pass |")
print("|---|---|---:|---:|---:|---:|---:|:---:|")
for page_label, sizes in results.items():
    for vp_label, r in sizes.items():
        if 'error' in r:
            print(f"| {page_label} | {vp_label} | ERROR | - | - | - | - | ❌ |")
            continue
        ox = r['overflowX']
        ov = len(r['overflowers'])
        wr = len(r['wraps'])
        fl = len(r['flyOuts'])
        bi = len(r['brokenImgs'])
        passed = ox == 0 and ov == 0 and wr == 0 and fl == 0 and bi == 0
        print(f"| {page_label} | {vp_label} | {ox} | {ov} | {wr} | {fl} | {bi} | {'✅' if passed else '⚠️'} |")
