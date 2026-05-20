#!/usr/bin/env python3
"""
全HTMLから LP特有の CTA FINAL セクションを除去。

対象パターン:
- <section class="cta-final"...>...</section>
- <section id="contact" class="cta-final"...>...</section>

コーポレートHPでは page 末尾のプロモーション CTA は付けない方針。
お問い合わせは header nav の通常リンクとフッターからアクセスする。

実行: python3 scripts/remove_cta_blocks.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PATTERNS = [
    # cta-final セクション
    re.compile(r'<section[^>]*class="[^"]*cta-final[^"]*"[^>]*>.*?</section>\s*', re.DOTALL),
    # cta-band を含む section（aria-label="お問い合わせCTA" 等）
    re.compile(r'<!--\s*CTA[^>]*-->\s*<section[^>]*>\s*<div class="cta-band">.*?</section>\s*', re.DOTALL),
    re.compile(r'<section[^>]*>\s*<div class="cta-band">.*?</section>\s*', re.DOTALL),
]

updated = 0
for p in DOCS.rglob("*.html"):
    text = p.read_text(encoding="utf-8")
    original = text
    for pat in PATTERNS:
        text = pat.sub('', text)
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"  ✓ {p.relative_to(DOCS)}")
        updated += 1
print(f"\n[OK] {updated} files cleaned")
