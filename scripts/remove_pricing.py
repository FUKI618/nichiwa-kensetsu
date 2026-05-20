#!/usr/bin/env python3
"""
価格情報を全HTMLから除去する。
理由: コーポレートHPからは価格を切り離し、LP側で扱う方針。

対象:
- index.html: PRICING セクション、JSON-LD makesOffer、価格言及テキスト
- services/*.html: 価格目安テーブル、価格言及メタタグ、ページ内テキスト
- contact.html / recruit.html / privacy.html: フッターの「料金プラン」リンク

実行: python3 scripts/remove_pricing.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# ============================================================
# 1) docs/index.html: PRICING セクション全削除 + JSON-LD makesOffer 削除
#    + 価格言及テキスト書き換え
# ============================================================

def fix_index():
    path = DOCS / "index.html"
    text = path.read_text(encoding="utf-8")

    # (a) JSON-LD makesOffer 配列を削除
    text = re.sub(
        r',\s*"makesOffer":\s*\[.*?\]',
        '',
        text,
        flags=re.DOTALL,
    )

    # (b) 解体工事 description の価格言及を書き換え
    text = text.replace(
        '"description": "木造・鉄骨・RC造・プチ解体まで全工種対応。20坪67.8万円〜の明朗価格と近隣合意形成を最優先。"',
        '"description": "木造・鉄骨・RC造・部分解体まで全工種対応。近隣合意形成を契約より先に。1,000件超の現場経験。"',
    )

    # (c) service card description の価格言及を書き換え
    text = text.replace(
        '木造、鉄骨、RC、そしてプチ解体まで。20坪 67.8 万円〜の明朗価格と、近隣を歩いて挨拶する地道な合意形成。「壊す」を雑にしない、それが日和の作法です。',
        '木造、鉄骨、RC、そして部分解体まで全工種対応。近隣を歩いて挨拶する地道な合意形成と、現場で積み上げた施工管理。「壊す」を雑にしない、それが日和の作法です。',
    )

    # (d) PRICING セクション削除（コメントマーカーで識別）
    text = re.sub(
        r'<!-- =+\s*\n\s*PRICING.*?<!-- (?==+\s*\n\s*FLOW)',
        '<!-- ',
        text,
        flags=re.DOTALL,
    )

    # (e) フッターの「料金プラン」リンク削除
    text = re.sub(
        r'\s*<li><a href="#pricing">料金プラン</a></li>',
        '',
        text,
    )

    path.write_text(text, encoding="utf-8")
    print(f"✓ index.html")


# ============================================================
# 2) docs/services/demolition.html: 価格目安テーブルから "From XX 万円" 削除
#    + JSON-LD offers 削除 + meta/lede 書き換え
# ============================================================

def fix_demolition():
    path = DOCS / "services" / "demolition.html"
    text = path.read_text(encoding="utf-8")

    # (a) meta description / og:description / og:title から価格削除
    text = text.replace(
        '<meta name="description" content="大阪・堺の解体工事。木造67.8万円〜、鉄骨127.8万円〜、RC造137.8万円〜、プチ解体5万円〜。1,000件超の実績、近隣との合意形成を契約より先に。大阪府知事 解体業許可 第1494号。" />',
        '<meta name="description" content="大阪・堺の解体工事。木造／鉄骨／RC造／部分解体まで全工種対応。1,000件超の実績、近隣との合意形成を契約より先に。大阪府知事 解体業許可 第1494号。" />',
    )
    text = text.replace(
        '<meta property="og:description" content="1,000件超の実績、近隣合意を契約より先に。20坪67.8万円〜の明朗価格。" />',
        '<meta property="og:description" content="1,000件超の実績、近隣合意を契約より先に。木造／鉄骨／RC造／部分解体まで全工種対応。" />',
    )

    # (b) page-hero lede 書き換え
    text = text.replace(
        '木造・鉄骨・RC造・プチ解体まで全工種に対応。20坪 67.8 万円〜の明朗価格と、契約前から始まる近隣合意形成。1,000 件超の現場で積み上げた、堺発の作法です。',
        '木造・鉄骨・RC造・部分解体まで全工種に対応。契約前から始まる近隣合意形成と、1,000 件超の現場で積み上げた、堺発の解体作法です。',
    )

    # (c) JSON-LD service description / offers
    text = text.replace(
        '"description": "木造・鉄骨・RC造・プチ解体に対応。20坪67.8万円〜の明朗価格、近隣合意形成を契約前から徹底。"',
        '"description": "木造・鉄骨・RC造・部分解体に対応。近隣合意形成を契約前から徹底し、1,000件超の現場経験に基づく施工管理。"',
    )
    text = re.sub(
        r',\s*"offers":\s*\[.*?\]',
        '',
        text,
        flags=re.DOTALL,
    )

    # (d) Coverage spec table の "From XX 万円" subline 削除
    text = re.sub(
        r'<br />\s*<small style="font-family:var\(--ff-serif-en\); font-style:italic; font-size:14px; color:var\(--c-brass\);">From [0-9.]+ 万円</small>',
        '',
        text,
    )

    # (e) Coverage spec table 直上のリード文 書き換え
    text = text.replace(
        '<p class="section-lede reveal">下表は 20 坪を基準とした参考価格です。地中障害物・産廃・足場・重機回送費等は別途。現地調査の無料見積りで、最終金額を必ず文書でお出しします。</p>',
        '<p class="section-lede reveal">木造から鉄骨・RC、部分解体まで。それぞれの工種で求められる段取り・養生・廃材分別の違いに合わせて、現場ごとに最適な施工計画を組み立てます。</p>',
    )

    # (f) "対応する工種と、価格目安。" → "対応する工種と、施工の段取り。"
    text = text.replace(
        '対応する工種と、価格目安。',
        '対応する工種と、施工の段取り。',
    )

    # (g) フッター「料金プラン」削除
    text = re.sub(r'\s*<li><a href="index\.html#pricing">料金プラン</a></li>', '', text)

    path.write_text(text, encoding="utf-8")
    print(f"✓ services/demolition.html")


# ============================================================
# 3) docs/services/asbestos.html: 価格目安削除
# ============================================================

def fix_asbestos():
    path = DOCS / "services" / "asbestos.html"
    text = path.read_text(encoding="utf-8")

    # 価格目安テーブル見出し書き換え
    text = text.replace(
        '対応するアスベストのレベルと、料金目安。',
        '対応するアスベストのレベルと、対応範囲。',
    )
    # th header「対象建材・特徴 ／ 料金目安」→「対象建材・特徴」
    text = text.replace(
        '<tr><th>レベル</th><th>対象建材・特徴 ／ 料金目安</th></tr>',
        '<tr><th>レベル</th><th>対象建材・特徴と対応範囲</th></tr>',
    )
    # JSON-LD makesOffer / offers / priceSpecification 配列があれば削除
    text = re.sub(r',\s*"offers":\s*\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r',\s*"makesOffer":\s*\[.*?\]', '', text, flags=re.DOTALL)
    # 「From XX 万円」「目安価格 XX 万円」テキスト削除
    text = re.sub(r'目安(?:価格)?[:：]?\s*[0-9０-９,，.]+\s*万円(?:〜|から)?', '対応', text)
    text = re.sub(r'From\s*[0-9.]+\s*万円', '対応', text)
    # フッター
    text = re.sub(r'\s*<li><a href="index\.html#pricing">料金プラン</a></li>', '', text)

    path.write_text(text, encoding="utf-8")
    print(f"✓ services/asbestos.html")


# ============================================================
# 4) docs/services/coating.html: 価格目安削除
# ============================================================

def fix_coating():
    path = DOCS / "services" / "coating.html"
    text = path.read_text(encoding="utf-8")

    text = text.replace('対応工事と、料金目安。', '対応工事と、施工の作法。')
    text = text.replace(
        '<tr><th>工事種別</th><th>内容・料金目安</th></tr>',
        '<tr><th>工事種別</th><th>内容と施工範囲</th></tr>',
    )
    # section aria-label
    text = text.replace('aria-label="対応工事と料金"', 'aria-label="対応工事と施工範囲"')
    text = re.sub(r',\s*"offers":\s*\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r',\s*"makesOffer":\s*\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'目安(?:価格)?[:：]?\s*[0-9０-９,，.]+\s*万円(?:〜|から)?', '対応', text)
    text = re.sub(r'From\s*[0-9.]+\s*万円', '対応', text)
    text = re.sub(r'\s*<li><a href="index\.html#pricing">料金プラン</a></li>', '', text)

    path.write_text(text, encoding="utf-8")
    print(f"✓ services/coating.html")


# ============================================================
# 5) docs/services/index.html: 価格言及削除
# ============================================================

def fix_services_index():
    path = DOCS / "services" / "index.html"
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        '解体工事・アスベスト除去・塗装外壁の3事業。木造67.8万円〜の明朗価格、レベル1〜3対応のアスベスト除去、創業由来の塗装事業。',
        '解体工事・アスベスト除去・塗装外壁の3事業。レベル1〜3対応のアスベスト除去、創業由来の塗装事業、近隣合意を契約より先に。',
    )
    text = text.replace(
        '木造・鉄骨・RC造・プチ解体まで全工種対応。20坪67.8万円〜の明朗価格、近隣を歩いて挨拶する地道な合意形成。「壊す」を雑にしない、それが日和の作法です。',
        '木造・鉄骨・RC造・部分解体まで全工種対応。近隣を歩いて挨拶する地道な合意形成と、現場で積み上げた施工管理。「壊す」を雑にしない、それが日和の作法です。',
    )

    path.write_text(text, encoding="utf-8")
    print(f"✓ services/index.html")


# ============================================================
# 6) フッターに「料金プラン」が残る他ページの清掃
# ============================================================

def fix_footer_pricing_links():
    for p in DOCS.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        new = re.sub(r'\s*<li><a href="index\.html#pricing">料金プラン</a></li>', '', text)
        new = re.sub(r'\s*<li><a href="#pricing">料金プラン</a></li>', '', new)
        if new != text:
            p.write_text(new, encoding="utf-8")
            print(f"  ✓ footer link removed: {p.relative_to(DOCS)}")


def main():
    fix_index()
    fix_demolition()
    fix_asbestos()
    fix_coating()
    fix_services_index()
    fix_footer_pricing_links()
    print("\n[DONE] all pricing references removed")


if __name__ == "__main__":
    main()
