#!/usr/bin/env python3
"""
全HTMLのフッターの brand--footer ブロックを、テキストからロゴ画像へ置換。

実行: python3 scripts/update_footer_brand.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

OLD_PATTERN = re.compile(
    r'<span class="brand(?:\s+brand--footer)?"[^>]*>\s*'
    r'<span class="brand__jp"[^>]*>株式会社\s*日和建設</span>\s*'
    r'<span class="brand__en">NICHIWA KENSETSU</span>\s*'
    r'</span>',
    re.DOTALL,
)

NEW_BLOCK = '''<span class="brand brand--footer" aria-hidden="true">
          <img class="brand__logo" src="assets/img/brand/logo.png" alt="" width="200" height="40" loading="lazy" />
        </span>'''


def main():
    updated = 0
    for p in DOCS.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        new = OLD_PATTERN.sub(NEW_BLOCK, text, count=1)
        if new != text:
            p.write_text(new, encoding="utf-8")
            print(f"  ✓ {p.relative_to(DOCS)}")
            updated += 1
    print(f"\n[OK] {updated} files updated")


if __name__ == "__main__":
    main()
