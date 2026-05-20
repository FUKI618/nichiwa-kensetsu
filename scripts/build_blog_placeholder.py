#!/usr/bin/env python3
"""
/blog/index.html を「現在準備中」プレースホルダーで生成。
中身が入るまでは記事リストを出さない（架空記事は作らない）。
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "blog" / "index.html"

BODY = '''<section class="section">
  <div class="container">
    <div style="max-width:680px; margin: 64px auto; padding: 64px 0; text-align:center;">
      <p style="font-family:var(--ff-serif-en); font-style:italic; font-size:18px; color:var(--c-brass); margin-bottom:24px;">Coming soon</p>
      <h2 style="font-family:var(--ff-serif-jp); font-size:28px; font-weight:600; line-height:1.7; margin-bottom:32px;">現在、準備中です。</h2>
      <p style="font-size:15px; line-height:2.2; color:var(--c-text-mute);">日和建設のブログは現在準備中です。<br />施工レポートや現場からのお知らせを順次公開してまいります。今しばらくお待ちください。</p>
    </div>
  </div>
</section>
'''

def main():
    bc = breadcrumb_inline([("ホーム", "index.html"), ("ブログ", "")])
    html = head(
        "ブログ｜株式会社 日和建設",
        "日和建設のブログ。施工レポートや現場からのお知らせを順次公開してまいります。",
        "https://nichiwa-kensetu.com/blog/",
        "/assets/img/services/demolition.webp",
    )
    html += HEADER + "\n"
    html += page_hero(
        "ブログ", "BLOG",
        "ブログ。",
        "Blog",
        "施工レポートや現場からのお知らせを、順次公開してまいります。",
        "assets/img/services/demolition.webp",
        bc,
    )
    html += BODY
    html += FOOTER
    html += "\n</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ {OUT.relative_to(ROOT)} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
