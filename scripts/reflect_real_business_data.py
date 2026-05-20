#!/usr/bin/env python3
"""
元サイトの実テキストで /services/* と /works/index.html を再構築。
架空の「OUR EDGE 3 benefits」「COVERAGE 価格目安」等のLP訴求ブロックは
全て削除し、元サイトの短文ベースで素直に組み直す。

実データ取得元:
- /business/dismantling/  → 解体事業 短文 (3行)
- /business/as/           → アスベスト事業 短文 + 18件実績テーブル
- /business/painting/     → 塗装事業 短文
- /business/ + 各事業ページ → 直近6件の施工実績タイトル
- /faq/                   → FAQ 5問 (実Q&A)

実行: python3 scripts/reflect_real_business_data.py
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# ============================================================
# 直近6件の施工実績 (元サイト /business/ 共通フッター掲載分)
# ============================================================
RECENT_WORKS = [
    {"date": "2025.01.24", "category": "解体", "title": "文化住宅 2階建 解体工事"},
    {"date": "2025.01.24", "category": "解体", "title": "秦和ビル 解体工事"},
    {"date": "2025.01.23", "category": "解体", "title": "大阪シティバス 解体工事"},
    {"date": "2025.01.23", "category": "解体・石綿", "title": "法隆寺幼稚園 解体・石綿除去工事"},
    {"date": "2025.01.22", "category": "解体・石綿", "title": "宝塚グリーンハイツ 解体工事・石綿除去工事"},
    {"date": "2025.01.22", "category": "階上解体", "title": "仁徳ビル 階上解体工事"},
]

def recent_works_grid_html(image_prefix="assets/img/works/work"):
    items = []
    for i, w in enumerate(RECENT_WORKS, 1):
        img = f"{image_prefix}-0{(i-1)%2+1}.webp"  # rotate between work-01.webp / work-02.webp
        items.append(f'''      <article class="card-work" style="background: var(--c-paper); color: var(--c-ink);">
        <div class="card-work__media">
          <img src="{img}" alt="{w["title"]}" width="800" height="600" loading="lazy" />
        </div>
        <h3 class="card-work__title" style="color: var(--c-ink); padding: 24px 24px 8px;">{w["title"]}</h3>
        <p class="card-work__meta" style="padding: 0 24px 24px;"><span>{w["category"]}</span><span>{w["date"]}</span></p>
      </article>''')
    return "\n".join(items)

# ============================================================
# /services/index.html
# ============================================================
SERVICES_INDEX = '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">SERVICES</span>
    <h2 class="section-title reveal">三つの事業領域。</h2>
    <p class="section-lede reveal">建築リフォームから始まった日和建設の事業は、解体工事業・アスベスト工事業・塗装工事業の三つに広がりました。それぞれの現場で、近隣への配慮と環境保全を最優先に取り組んでいます。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/demolition.webp" alt="解体事業" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">No. 01</span>
          <h3 class="card-service__title">解体事業<small>DISMANTLING</small></h3>
          <p class="card-service__desc">建築リフォームと同時に解体工事業を自社で請け負っております。近隣への挨拶はもちろん、町を汚さないよう、環境への配慮を忘れずに作業を行うよう、職人全員に指導をしております。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="services/demolition.html">解体事業を見る</a>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/asbestos.webp" alt="アスベスト工事業" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">No. 02</span>
          <h3 class="card-service__title">アスベスト工事業<small>ASBESTOS</small></h3>
          <p class="card-service__desc">アスベスト対策を重要な社会問題と捉え、適正な除去・処理を行うとともに、大気汚染防止に努め、環境保全に貢献していきます。作業に従事する従業員と家族の健康を守るため、安全な作業環境作りも行っています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="services/asbestos.html">アスベスト工事業を見る</a>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/coating.webp" alt="塗装工事業" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">No. 03</span>
          <h3 class="card-service__title">塗装工事業<small>COATING</small></h3>
          <p class="card-service__desc">私たちは塗装の技術だけではなく、外壁の知識も磨き上げようと常に前向きに作業を行っております。日和建設 外壁診断のプロによる診断を、ぜひ一度お試しください。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="services/coating.html">塗装工事業を見る</a>
        </div>
      </article>
    </div>
  </div>
</section>
'''

# ============================================================
# /services/demolition.html
# ============================================================
DEMOLITION_BODY = '''<section class="section">
  <div class="container">
    <div style="max-width:780px; margin-bottom:64px;">
      <p class="section-lede reveal" style="font-size:17px; line-height:2.2;">建築リフォームと同時に解体工事業を自社で請け負っております。近隣への挨拶はもちろん、町を汚さないよう、環境への配慮を忘れずに作業を行うよう、職人全員に指導をしております。</p>
    </div>

    <span class="eyebrow reveal">RECENT WORKS</span>
    <h2 class="section-title reveal">直近の施工実績。</h2>
    <div class="services-grid reveal-stagger" style="margin-top:48px;">
''' + recent_works_grid_html() + '''
    </div>
  </div>
</section>
'''

# ============================================================
# /services/asbestos.html
# ============================================================
ASBESTOS_HISTORY = [
    ("2021", "桜塚ハイツ アスベスト除去工事", "1ヶ月"),
    ("2021", "垂水区 一軒家 アスベスト除去工事", "14日"),
    ("2022", "エバーケミカル工業㈱ 外壁アスベスト除去工事", "14日"),
    ("2022", "株式会社ヤマタネ 危険物定温倉庫 外壁アスベスト除去工事", "20日"),
    ("2022", "橿原市 平田様邸 建物アスベスト除去工事", "10日"),
    ("2022", "株式会社五十君様邸 アスベスト除去工事", "20日"),
    ("2022", "ダクタリ動物病院 アスベスト除去工事", "1ヶ月"),
    ("2022", "木川東 鉄骨造3階建 アスベスト除去工事", "1ヶ月"),
    ("2022", "淀川ビル 吹き付け石綿除去工事", "1ヶ月"),
    ("2022", "鈴蘭台交番 外壁アスベスト除去工事", "15日"),
    ("2022", "岡山県 ロッソ 吹付石綿除去工事", "2ヶ月"),
    ("2022", "尼崎市 RC2階 石綿除去工事", "20日"),
    ("2022", "高島屋京都店 吹付石綿除去工事", "1か月"),
    ("2022", "滋賀県 ロイヤルウォーク 石綿除去工事", "3か月"),
    ("2022", "石ケ辻町 外壁石綿除去工事", "20日"),
    ("2022", "旧阿倍野桃ヶ池町 社宅 外壁石綿除去工事", "20日"),
    ("2022", "青森県 米軍基地 石綿除去工事", "4ヶ月"),
    ("2022", "町田第一マンション 外壁石綿除去工事", "1ヶ月"),
]
ASBESTOS_ROWS = "\n".join(
    f'        <tr><td>{y}</td><td>{name}</td><td style="text-align:right; font-family:var(--ff-sans-en); color:var(--c-brass);">{dur}</td></tr>'
    for y, name, dur in ASBESTOS_HISTORY
)
ASBESTOS_BODY = f'''<section class="section">
  <div class="container">
    <div style="max-width:780px; margin-bottom:64px;">
      <p class="section-lede reveal" style="font-size:17px; line-height:2.2;">アスベスト対策を重要な社会問題と捉え、適正な除去・処理を行うとともに、大気汚染防止に努め、環境保全に貢献していきます。作業に従事する従業員と家族の健康を守るため、安全な作業環境作りも行っています。</p>
      <p class="reveal" style="margin-top:24px; font-size:15px; line-height:2; color: var(--c-text-mute);">アスベスト工事業は、環境への配慮が一番に必要な事業です。より一層気を引き締め、安全な環境作りのため尽力いたします。</p>
    </div>

    <span class="eyebrow reveal">PROJECT HISTORY</span>
    <h2 class="section-title reveal">アスベスト除去工事 実績。</h2>
    <p class="section-lede reveal" style="margin-top:16px;">2021年〜2022年にかけて施工させていただいた18件の記録です。</p>

    <div style="margin-top:48px; overflow-x:auto;">
      <table class="company-table" style="width:100%;">
        <thead>
          <tr><th style="width:80px;">年</th><th>工事名称</th><th style="width:120px; text-align:right;">工期</th></tr>
        </thead>
        <tbody>
{ASBESTOS_ROWS}
        </tbody>
      </table>
    </div>
  </div>
</section>
'''

# ============================================================
# /services/coating.html
# ============================================================
COATING_BODY = '''<section class="section">
  <div class="container">
    <div style="max-width:780px; margin-bottom:64px;">
      <p class="section-lede reveal" style="font-size:17px; line-height:2.2;">私たちは塗装の技術だけではなく、外壁の知識も磨き上げようと常に前向きに作業を行っております。日和建設 外壁診断のプロによる診断を、ぜひ一度お試しください。</p>
    </div>

    <span class="eyebrow reveal">SCOPE</span>
    <h2 class="section-title reveal">対応工事。</h2>

    <div style="margin-top:48px; display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:32px;">
      <div>
        <strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">EXTERIOR ／ 外壁</strong>
        <p style="margin-top:12px; line-height:2;">外壁塗装、外壁補修、シール（シーリング）工事。マンション・一般住宅の請負実績あり。</p>
      </div>
      <div>
        <strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">SCAFFOLDING ／ 足場</strong>
        <p style="margin-top:12px; line-height:2;">足場工事を一式対応。塗装・防水・外壁工事の前段階として設計・施工。</p>
      </div>
      <div>
        <strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">WATERPROOF ／ 防水</strong>
        <p style="margin-top:12px; line-height:2;">屋上・バルコニー・外壁の防水工事。塗装工事との一体施工が可能です。</p>
      </div>
    </div>
  </div>
</section>
'''

# ============================================================
# /works/index.html — 直近6件の実施工実績
# ============================================================
WORKS_INDEX_BODY = '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">RECENT WORKS</span>
    <h2 class="section-title reveal">直近の施工実績。</h2>
    <p class="section-lede reveal">2025年1月時点で公開している、直近の施工実績です。詳細は元サイト nichiwa-kensetu.com の各実績ページからご覧いただけます。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
''' + recent_works_grid_html() + '''
    </div>
  </div>
</section>
'''


PAGES = {
    "services/index.html": {
        "title": "事業内容｜株式会社 日和建設",
        "description": "解体事業・アスベスト工事業・塗装工事業の三つの事業領域。建築リフォームから始まった日和建設の事業内容をご紹介します。",
        "canonical": "https://nichiwa-kensetu.com/services/",
        "category": "事業内容",
        "category_en": "SERVICES",
        "h1": "事業内容。",
        "h1_en": "Services",
        "lede": "建築リフォームから始まった日和建設の事業は、解体工事業・アスベスト工事業・塗装工事業の三つに広がりました。",
        "bg": "assets/img/services/demolition.webp",
        "breadcrumb": [("ホーム", "index.html"), ("事業内容", "")],
        "body": SERVICES_INDEX,
    },
    "services/demolition.html": {
        "title": "解体事業｜株式会社 日和建設",
        "description": "建築リフォームと同時に解体工事業を自社で請け負っております。近隣への挨拶と環境への配慮を、職人全員に指導しております。",
        "canonical": "https://nichiwa-kensetu.com/services/demolition.html",
        "category": "解体事業",
        "category_en": "DISMANTLING",
        "h1": "解体事業。",
        "h1_en": "Dismantling",
        "lede": "建築リフォームと同時に解体工事業を自社で請け負っております。近隣への挨拶はもちろん、町を汚さないよう、環境への配慮を忘れずに作業を行うよう、職人全員に指導をしております。",
        "bg": "assets/img/services/demolition.webp",
        "breadcrumb": [("ホーム", "index.html"), ("事業内容", "services/"), ("解体事業", "")],
        "body": DEMOLITION_BODY,
    },
    "services/asbestos.html": {
        "title": "アスベスト工事業｜株式会社 日和建設",
        "description": "アスベスト対策を重要な社会問題と捉え、適正な除去・処理を行います。2021〜2022年の施工実績18件を公開。",
        "canonical": "https://nichiwa-kensetu.com/services/asbestos.html",
        "category": "アスベスト工事業",
        "category_en": "ASBESTOS",
        "h1": "アスベスト工事業。",
        "h1_en": "Asbestos",
        "lede": "アスベスト対策を重要な社会問題と捉え、適正な除去・処理を行うとともに、大気汚染防止に努め、環境保全に貢献していきます。",
        "bg": "assets/img/services/asbestos.webp",
        "breadcrumb": [("ホーム", "index.html"), ("事業内容", "services/"), ("アスベスト工事業", "")],
        "body": ASBESTOS_BODY,
    },
    "services/coating.html": {
        "title": "塗装工事業｜株式会社 日和建設",
        "description": "塗装の技術だけでなく、外壁の知識も磨き上げる日和建設の塗装工事業。外壁・足場・防水の一式対応。",
        "canonical": "https://nichiwa-kensetu.com/services/coating.html",
        "category": "塗装工事業",
        "category_en": "COATING",
        "h1": "塗装工事業。",
        "h1_en": "Coating",
        "lede": "塗装の技術だけではなく、外壁の知識も磨き上げようと常に前向きに作業を行っております。日和建設 外壁診断のプロによる診断を、ぜひ一度お試しください。",
        "bg": "assets/img/services/coating.webp",
        "breadcrumb": [("ホーム", "index.html"), ("事業内容", "services/"), ("塗装工事業", "")],
        "body": COATING_BODY,
    },
    "works/index.html": {
        "title": "施工事例｜株式会社 日和建設",
        "description": "日和建設の直近の施工事例。文化住宅・秦和ビル・大阪シティバス・法隆寺幼稚園・宝塚グリーンハイツ・仁徳ビルの解体工事ほか。",
        "canonical": "https://nichiwa-kensetu.com/works/",
        "category": "施工事例",
        "category_en": "WORKS",
        "h1": "施工事例。",
        "h1_en": "Works",
        "lede": "2025年1月時点で公開している、直近の施工実績です。",
        "bg": "assets/img/works/work-01.webp",
        "breadcrumb": [("ホーム", "index.html"), ("施工事例", "")],
        "body": WORKS_INDEX_BODY,
    },
}


def main():
    for rel, cfg in PAGES.items():
        path = DOCS / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        bc = breadcrumb_inline(cfg["breadcrumb"])
        html = head(cfg["title"], cfg["description"], cfg["canonical"], "/" + cfg["bg"])
        html += HEADER + "\n"
        html += page_hero(cfg["category"], cfg["category_en"], cfg["h1"], cfg["h1_en"], cfg["lede"], cfg["bg"], bc)
        html += cfg["body"]
        html += FOOTER
        html += "\n</body>\n</html>\n"
        path.write_text(html, encoding="utf-8")
        print(f"✓ {rel} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
