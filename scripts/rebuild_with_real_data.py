#!/usr/bin/env python3
"""
[ARCHIVED] /company/ 配下のサブページ個別生成スクリプト。

旧構成: /company/message.html, profile.html, history.html, offices.html,
       employees.html, license.html を個別に生成していた。

新構成: 全コンテンツを /company/index.html 単一ページに統合
        (scripts/build_unified_company.py が新しい所有者)

このスクリプトは now-noop。互換性のため残してあるが、
PAGES は空辞書なので何も生成しない。

実行: python3 scripts/rebuild_with_real_data.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PAGES = {}  # Intentionally empty — see build_unified_company.py


def main():
    if PAGES:
        from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline  # noqa
        # (no-op while PAGES is empty)
    print("[OK] rebuild_with_real_data.py is a no-op now — see build_unified_company.py")


if __name__ == "__main__":
    main()
