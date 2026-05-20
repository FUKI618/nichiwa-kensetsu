#!/usr/bin/env python3
"""
削除した /works/ への参照を全HTMLから除去。

- フッターの「<li><a href="works/">施工事例</a></li>」→「ブログ」(/blog/) へ書き換え
- /services/demolition.html の RECENT WORKS card grid セクションを削除
  （/works/ 配下が無くなった + 施工事例はブログ形式の準備中ページ）

実行: python3 scripts/cleanup_works_refs.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

updated = 0
for p in DOCS.rglob("*.html"):
    text = p.read_text(encoding="utf-8")
    original = text

    # Footer 施工事例 → ブログ
    text = text.replace(
        '<li><a href="works/">施工事例</a></li>',
        '<li><a href="blog/">ブログ</a></li>',
    )

    # demolition.html の RECENT WORKS section（card-work グリッド + 見出し）を削除
    if p.name == "demolition.html":
        text = re.sub(
            r'\s*<span class="eyebrow reveal">RECENT WORKS</span>.*?</div>\s*</div>\s*</section>',
            '',
            text,
            flags=re.DOTALL,
        )

    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"  ✓ {p.relative_to(DOCS)}")
        updated += 1

print(f"\n[OK] {updated} files updated")
