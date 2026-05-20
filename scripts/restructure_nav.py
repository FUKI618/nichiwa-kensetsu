#!/usr/bin/env python3
"""
日和建設 IA リストラクチャ — recruit.co.jp フォーマット模倣
全HTMLページのグローバルナビを刷新（6項目 → 7項目、recruit.co.jp 同形式）。

実行: python3 scripts/restructure_nav.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

NEW_HEADER = '''<header class="site-header" role="banner">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="株式会社 日和建設 トップ">
      <img class="brand__logo" src="assets/img/brand/logo.png" alt="株式会社 日和建設" width="200" height="40" loading="eager" />
    </a>

    <nav class="global-nav" aria-label="グローバルナビゲーション">
      <a href="company/">企業情報</a>
      <a href="services/">事業内容</a>
      <a href="works/">施工事例</a>
      <a href="sustainability/">サステナビリティ</a>
      <a href="culture/">人的資本経営</a>
      <a href="blog/">ブログ</a>
      <a href="news/">お知らせ</a>
      <a href="recruit.html">採用情報</a>
    </nav>

    <div class="header-actions">
      <a class="header-tel" href="tel:0722390126" aria-label="電話で問い合わせ 072-239-0126">
        <span>072-239-0126</span>
        <small>受付 8:00 – 19:00（日祝除く）</small>
      </a>
      <a class="btn btn-gold" href="contact.html">
        <span>無料 現地調査を依頼する</span>
        <span class="arrow" aria-hidden="true"></span>
      </a>
      <button type="button" class="menu-btn" aria-label="メニューを開く" aria-expanded="false" aria-controls="mobile-nav">
        <span class="bar" aria-hidden="true"></span>
      </button>
    </div>
  </div>
</header>

<nav id="mobile-nav" class="mobile-nav" aria-label="モバイルメニュー">
  <ul>
    <li><a href="company/">企業情報<small>COMPANY</small></a></li>
    <li><a href="company/philosophy.html">経営理念<small>PHILOSOPHY</small></a></li>
    <li><a href="company/message.html">代表メッセージ<small>MESSAGE</small></a></li>
    <li><a href="services/">事業内容<small>SERVICES</small></a></li>
    <li><a href="services/demolition.html">解体工事<small>DEMOLITION</small></a></li>
    <li><a href="services/asbestos.html">アスベスト除去<small>ASBESTOS</small></a></li>
    <li><a href="services/coating.html">塗装・外壁工事<small>COATING</small></a></li>
    <li><a href="works/">施工事例<small>WORKS</small></a></li>
    <li><a href="sustainability/">サステナビリティ<small>SUSTAINABILITY</small></a></li>
    <li><a href="culture/">人的資本経営<small>OUR PEOPLE</small></a></li>
    <li><a href="strengths/">私たちの強み<small>STRENGTHS</small></a></li>
    <li><a href="blog/">ブログ<small>BLOG</small></a></li>
    <li><a href="news/">お知らせ<small>NEWS</small></a></li>
    <li><a href="company/profile.html">会社概要<small>PROFILE</small></a></li>
    <li><a href="recruit.html">採用情報<small>RECRUIT</small></a></li>
    <li><a href="contact.html">お問い合わせ<small>CONTACT</small></a></li>
  </ul>
  <div class="mobile-nav__cta">
    <a class="btn btn-gold" href="contact.html"><span>無料 現地調査を依頼する</span><span class="arrow" aria-hidden="true"></span></a>
    <a class="btn btn-ghost" href="tel:0722390126"><span>072-239-0126 ／ 受付 8:00–19:00</span></a>
  </div>
</nav>'''


# Regex matches existing header through mobile-nav (any variant) — non-greedy
HEADER_PATTERN = re.compile(
    r'<header class="site-header[^"]*"[^>]*>.*?</nav>\s*(?=<!--|\n<section|\n<main)',
    re.DOTALL,
)

# Fallback pattern for pages where mobile-nav ends just before another tag
HEADER_PATTERN_LOOSE = re.compile(
    r'<header class="site-header[^"]*"[^>]*>.*?</nav>',
    re.DOTALL,
)


def process(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    # Try strict first
    new_text, n = HEADER_PATTERN.subn(NEW_HEADER + "\n", text, count=1)
    if n == 0:
        # Try loose (replace just first occurrence; mobile-nav comes right after header)
        # Actually each page has TWO matches: the desktop header, then the mobile-nav.
        # We want to replace BOTH with the single NEW_HEADER block.
        # Strategy: find header start, find SECOND </nav> (closing mobile-nav), replace span.
        match = re.search(r'<header class="site-header', text)
        if not match:
            return False, "no <header> found"
        start = match.start()
        # find all </nav>
        nav_closes = [m.end() for m in re.finditer(r'</nav>', text)]
        # Pick the second one (which closes mobile-nav). If only one, take the first.
        if len(nav_closes) >= 2:
            end = nav_closes[1]
        elif len(nav_closes) >= 1:
            end = nav_closes[0]
        else:
            return False, "no </nav> found"
        new_text = text[:start] + NEW_HEADER + text[end:]
    if new_text == text:
        return False, "no change"
    path.write_text(new_text, encoding="utf-8")
    return True, "ok"


def main():
    htmls = sorted(DOCS.rglob("*.html"))
    for p in htmls:
        ok, msg = process(p)
        rel = p.relative_to(DOCS)
        print(f"{'✓' if ok else '✗'} {rel}: {msg}")


if __name__ == "__main__":
    main()
