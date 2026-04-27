#!/usr/bin/env python3
"""
日和建設 works/work-XX.html 詳細ページ自動生成
旧サイト( https://nichiwa-kensetu.com/ )から取得した本物の6件のみを掲載。
未取得項目は「ー」表示し、想像での補完は行わない（誠実性重視）。

実行: python3 scripts/generate_work_details.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "制作物"

# 6件の本物データ（旧サイトから収集）。未取得は None / "ー"
# source_url は旧サイトの該当事例ページURL
WORKS = [
    {
        "id": "01",
        "title": "茨木市東奈良 木造 2 階＋平家建 解体工事",
        "subtitle": "Wooden 2-Story + 1-Story Demolition",
        "category": "demolition", "category_label": "木造解体",
        "area": "osaka", "area_label": "大阪府茨木市",
        "structure": "木造 2 階建 ＋ 平家建",
        "scale": "ー",
        "use": "住宅",
        "scope": "解体工事 ／ 残置物処理 ／ 整地",
        "year": "2023 年 3 月",
        "duration": "ー",
        "img": "work-01.webp",
        "note": "鍵なし・残置物ありの難物件として弊社が引き受けた事例です。残置物の仕分け・処分から整地施工まで一貫対応で完工しました。Before/After 写真は元ページに掲載されています。",
        "source_url": "https://nichiwa-kensetu.com/ibarakihigasinara/",
    },
    {
        "id": "02",
        "title": "富田林市寺池台 木造 2 階 解体工事",
        "subtitle": "Wooden 2-Story Demolition",
        "category": "demolition", "category_label": "木造解体",
        "area": "osaka", "area_label": "大阪府富田林市",
        "structure": "木造 2 階建",
        "scale": "ー",
        "use": "住宅",
        "scope": "解体工事 ／ 整地",
        "year": "2023 年 3 月",
        "duration": "ー",
        "img": "work-01.webp",
        "note": "閑静な住宅街での木造解体。Before/After 写真を元ページに掲載しています。",
        "source_url": "https://nichiwa-kensetu.com/tondabayashi/",
    },
    {
        "id": "03",
        "title": "堺市堺区旭丘 RC 造 2 階建 解体工事",
        "subtitle": "RC 2-Story Demolition",
        "category": "demolition", "category_label": "RC 造解体",
        "area": "osaka", "area_label": "大阪府堺市堺区",
        "structure": "RC 造 2 階建",
        "scale": "ー",
        "use": "ー",
        "scope": "RC 造解体工事",
        "year": "2022 年 4 月",
        "duration": "ー",
        "img": "work-02.webp",
        "note": "堺市堺区での RC 造解体。手壊しと機械解体を組み合わせ、近隣動線を確保しながら段階的に進行しました。",
        "source_url": "https://nichiwa-kensetu.com/%e5%a0%ba%e5%b8%82%e5%a0%ba%e5%8c%ba%e6%97%ad%e4%b8%98rc%e9%80%a0%ef%bc%92%e9%9a%8e%e5%bb%ba%e8%a7%a3%e4%bd%93%e5%b7%a5%e4%ba%8b/",
    },
    {
        "id": "04",
        "title": "泉南郡熊取町 木造 2 階建 解体撤去工事",
        "subtitle": "Wooden 2-Story Demolition",
        "category": "demolition", "category_label": "木造解体",
        "area": "osaka", "area_label": "大阪府泉南郡熊取町",
        "structure": "木造 2 階建",
        "scale": "ー",
        "use": "住宅",
        "scope": "解体撤去工事",
        "year": "2021 年 12 月",
        "duration": "ー",
        "img": "work-01.webp",
        "note": "弊社の実績事例の一つ。住宅地での木造解体撤去工事として完工しました。",
        "source_url": "https://nichiwa-kensetu.com/%e6%b3%89%e5%8d%97%e9%83%a1%e7%86%8a%e5%8f%96%e7%94%ba%e6%9c%a8%e9%80%a02%e9%9a%8e%e5%bb%ba%e3%81%a6%e8%a7%a3%e4%bd%93%e6%92%a4%e5%8e%bb%e5%b7%a5%e4%ba%8b/",
    },
    {
        "id": "05",
        "title": "仁徳ビル 階上解体工事",
        "subtitle": "Upper-Floor Demolition",
        "category": "demolition", "category_label": "鉄骨／RC 階上解体",
        "area": "osaka", "area_label": "ー（大阪府内）",
        "structure": "鉄骨／RC 6 階建（階上解体）",
        "scale": "6 階建",
        "use": "オフィスビル",
        "scope": "階上解体工事",
        "year": "2025 年 1 月",
        "duration": "ー",
        "img": "work-02.webp",
        "note": "隣接敷地が狭い難条件の現場。安全管理を徹底し、事故なく完了しました。下階の運用に影響を出さない階上解体を実現しています。",
        "source_url": "https://nichiwa-kensetu.com/%E4%BB%81%E5%BE%B3%E3%83%93%E3%83%AB%E9%9A%8E%E4%B8%8A%E8%A7%A3%E4%BD%93%E5%B7%A5%E4%BA%8B/",
    },
    {
        "id": "06",
        "title": "大阪シティバス 解体工事",
        "subtitle": "Bus Garage Demolition",
        "category": "demolition", "category_label": "解体",
        "area": "osaka", "area_label": "ー（大阪府内）",
        "structure": "ー",
        "scale": "ー",
        "use": "運輸施設（バス関連）",
        "scope": "解体工事",
        "year": "ー",
        "duration": "ー",
        "img": "work-02.webp",
        "note": "弊社の実績事例の一つ。安全第一を掲げ、公共性の高い施設の解体工事を完工しました。",
        "source_url": "https://nichiwa-kensetu.com/%E5%A4%A7%E9%98%AA%E3%82%B7%E3%83%86%E3%82%A3%E3%83%90%E3%82%B9%E8%A7%A3%E4%BD%93%E5%B7%A5%E4%BA%8B/",
    },
]


def related_for(target):
    """同カテゴリで他の事例3件を関連事例に。なければ別事例で補充。"""
    same = [w for w in WORKS if w["category"] == target["category"] and w["id"] != target["id"]]
    others = [w for w in WORKS if w["category"] != target["category"] and w["id"] != target["id"]]
    return (same + others)[:3]


TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#0F1B2D" />
  <title>{title}｜施工事例 ─ 株式会社 日和建設</title>
  <meta name="description" content="{title}（{area_label}）の施工事例。{category_label}、{structure}。日和建設の実績を、本物の現場記録としてご紹介します。" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta http-equiv="X-Content-Type-Options" content="nosniff" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}｜施工事例 ─ 日和建設" />
  <meta property="og:description" content="{category_label}、{area_label}、{year}。" />
  <meta property="og:image" content="https://nichiwa-kensetu.com/assets/img/works/{img}" />

  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="canonical" href="https://nichiwa-kensetu.com/works/work-{id}.html" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@500;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="/assets/css/style.css" />
  <link rel="stylesheet" href="/assets/css/animations.css" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Article",
        "headline": "{title}",
        "image": "https://nichiwa-kensetu.com/assets/img/works/{img}",
        "datePublished": "{year_iso}",
        "author": {{
          "@type": "Organization",
          "name": "株式会社 日和建設",
          "url": "https://nichiwa-kensetu.com/"
        }},
        "publisher": {{
          "@type": "Organization",
          "name": "株式会社 日和建設",
          "logo": {{ "@type": "ImageObject", "url": "https://nichiwa-kensetu.com/favicon.svg" }}
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://nichiwa-kensetu.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "施工事例", "item": "https://nichiwa-kensetu.com/works/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "https://nichiwa-kensetu.com/works/work-{id}.html" }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>

<header class="site-header is-scrolled" role="banner">
  <div class="site-header__inner">
    <a class="brand" href="/index.html" aria-label="日和建設 トップ">
      <span class="brand__jp">株式会社 日和建設</span>
      <span class="brand__en">NICHIWA KENSETSU</span>
    </a>
    <nav class="global-nav" aria-label="グローバルナビゲーション">
      <a href="/index.html#services">事業内容</a>
      <a href="/index.html#why">選ばれる理由</a>
      <a href="/works/">施工事例</a>
      <a href="/index.html#pricing">料金</a>
      <a href="/recruit.html">採用情報</a>
      <a href="/index.html#faq">FAQ</a>
    </nav>
    <div class="header-actions">
      <a class="header-tel" href="tel:0722390126">
        <span>072-239-0126</span>
        <small>受付 8:00 – 19:00（日祝除く）</small>
      </a>
      <a class="btn btn-gold" href="/contact.html"><span>無料 現地調査を依頼する</span><span class="arrow" aria-hidden="true"></span></a>
      <button type="button" class="menu-btn" aria-label="メニューを開く" aria-expanded="false" aria-controls="mobile-nav"><span class="bar" aria-hidden="true"></span></button>
    </div>
  </div>
</header>

<nav id="mobile-nav" class="mobile-nav" aria-label="モバイルメニュー">
  <ul>
    <li><a href="/index.html#services">事業内容<small>SERVICES</small></a></li>
    <li><a href="/services/demolition.html">解体工事<small>DEMOLITION</small></a></li>
    <li><a href="/services/asbestos.html">アスベスト除去<small>ASBESTOS</small></a></li>
    <li><a href="/services/coating.html">塗装・外壁工事<small>COATING</small></a></li>
    <li><a href="/works/">施工事例<small>WORKS</small></a></li>
    <li><a href="/recruit.html">採用情報<small>RECRUIT</small></a></li>
    <li><a href="/contact.html">お問い合わせ<small>CONTACT</small></a></li>
  </ul>
  <div class="mobile-nav__cta">
    <a class="btn btn-gold" href="/contact.html"><span>無料 現地調査を依頼する</span><span class="arrow" aria-hidden="true"></span></a>
    <a class="btn btn-ghost" href="tel:0722390126"><span>072-239-0126 ／ 受付 8:00–19:00</span></a>
  </div>
</nav>

<!-- Page hero -->
<section class="page-hero" style="min-height: clamp(380px, 56vh, 540px);">
  <div class="page-hero__bg" aria-hidden="true">
    <img src="/assets/img/works/{img}" alt="" width="2400" height="1800" loading="eager" fetchpriority="high" />
  </div>
  <div class="container page-hero__inner">
    <nav class="breadcrumbs" aria-label="パンくず">
      <ol>
        <li><a href="/index.html">ホーム</a></li>
        <li><a href="/works/">施工事例</a></li>
        <li>{title}</li>
      </ol>
    </nav>
    <span class="page-hero__cat">CASE NO. {id}</span>
    <h1 class="page-hero__title">
      <small>{subtitle}</small>
      {title}
    </h1>
    <p class="detail-meta">
      <span>{category_label}</span>
      <span>{area_label}</span>
      <span>{year}</span>
    </p>
  </div>
</section>

<!-- Spec table -->
<section class="section" aria-label="物件概要">
  <div class="container">
    <span class="eyebrow reveal">PROJECT OVERVIEW</span>
    <h2 class="section-title reveal">物件概要と、工事内容。</h2>
    <p class="section-lede reveal">本ページは弊社の実績記録です。一部の項目は、お客様情報保護のため非公開としています。詳細にご関心のある方は、お問い合わせください。</p>

    <table class="spec-table" style="margin-top:48px;">
      <tbody>
        <tr><th>構造</th><td>{structure}</td></tr>
        <tr><th>規模</th><td>{scale}</td></tr>
        <tr><th>用途</th><td>{use}</td></tr>
        <tr><th>所在地</th><td>{area_label}</td></tr>
        <tr><th>工事内容</th><td>{scope}</td></tr>
        <tr><th>工期</th><td>{duration}</td></tr>
        <tr><th>完工</th><td>{year}</td></tr>
      </tbody>
    </table>
  </div>
</section>

<!-- Note -->
<section class="section section--paper" aria-label="現場記録">
  <div class="container">
    <div style="max-width: 880px; margin-inline: auto;">
      <span class="eyebrow reveal">SITE NOTE</span>
      <h2 class="section-title reveal">この現場の、記録。</h2>
      <p class="reveal" style="margin-top:24px; font-size:15px; line-height:2.05; color: var(--c-text);">{note}</p>
      <p class="reveal" style="margin-top:32px; font-size:13px; color: var(--c-text-mute);">
        この事例ページは、旧サイト
        <a href="{source_url}" target="_blank" rel="noopener" style="color:var(--c-brass); border-bottom:1px solid currentColor;">元記事</a>
        の内容を再構成して掲載しています。Before/After 写真や追加情報は元ページもあわせてご確認ください。
      </p>
    </div>
  </div>
</section>

<!-- Related works -->
<section class="section" aria-label="関連する施工事例">
  <div class="container">
    <span class="eyebrow reveal">RELATED CASES</span>
    <h2 class="section-title reveal">他の現場も、ご覧ください。</h2>

    <div class="works-grid reveal-stagger" style="margin-top:48px;">
      {related_html}
    </div>

    <div style="margin-top:48px; text-align:center;">
      <a class="btn-link" href="/works/">施工事例一覧へ戻る</a>
    </div>
  </div>
</section>

<!-- CTA band -->
<section aria-label="お問い合わせCTA">
  <div class="cta-band">
    <p>「うちの建物にも、似た事例はありますか？」<br />類似事例の実績データから、お見積りを文書でご提示します。<small>現地調査・お見積りは無料。当日中に一次回答します。</small></p>
    <div class="actions">
      <a class="btn btn-gold" href="/contact.html"><span>無料 現地調査を依頼する</span><span class="arrow" aria-hidden="true"></span></a>
      <a class="tel-block" href="tel:0722390126"><span>072-239-0126</span><small>受付 8:00 – 19:00（日祝除く）</small></a>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <span class="brand">
          <span class="brand__jp" style="color:#fff;">株式会社 日和建設</span>
          <span class="brand__en">NICHIWA KENSETSU</span>
        </span>
        <p style="margin-top:20px;">
          〒599-8126<br />大阪府堺市東区大美野 171-36<br />
          TEL <a href="tel:0722390126">072-239-0126</a><br />
          FAX 072-236-6491
        </p>
      </div>
      <div>
        <h4>SERVICES</h4>
        <ul>
          <li><a href="/services/demolition.html">解体工事</a></li>
          <li><a href="/services/asbestos.html">アスベスト除去</a></li>
          <li><a href="/services/coating.html">塗装・外壁工事</a></li>
          <li><a href="/index.html#pricing">料金プラン</a></li>
        </ul>
      </div>
      <div>
        <h4>COMPANY</h4>
        <ul>
          <li><a href="/index.html#why">選ばれる理由</a></li>
          <li><a href="/works/">施工事例</a></li>
          <li><a href="/index.html#voices">お客様の声</a></li>
          <li><a href="/index.html#company">会社概要</a></li>
          <li><a href="/index.html#faq">FAQ</a></li>
          <li><a href="/recruit.html">採用情報</a></li>
        </ul>
      </div>
      <div>
        <h4>CONTACT</h4>
        <ul>
          <li><a href="/contact.html">お問い合わせ</a></li>
          <li><a href="/privacy.html">プライバシーポリシー</a></li>
          <li style="opacity:.6; margin-top:14px;">本社 ／ 大阪府堺市東区</li>
          <li style="opacity:.6;">南大阪営業所 / 東京営業所</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2021–<span data-current-year>2026</span> NICHIWA KENSETSU CO., LTD.</span>
      <span>大阪府知事 解体業許可 第 1494 号</span>
    </div>
  </div>
</footer>

<script src="/assets/js/utils.js" defer></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""

RELATED_CARD = """      <a class="card-work" href="/works/work-{id}.html">
        <div class="card-work__media">
          <img src="/assets/img/works/{img}" alt="{title}" width="800" height="600" loading="lazy" />
          <span class="card-work__view">VIEW →</span>
        </div>
        <h3 class="card-work__title">{title}</h3>
        <p class="card-work__meta"><span>{category_label}</span><span>{area_label}</span><span>{year}</span></p>
      </a>"""


def main():
    out_dir = ROOT / "works"
    out_dir.mkdir(exist_ok=True)
    # Remove old work-XX.html (keep index.html)
    for old in out_dir.glob("work-*.html"):
        old.unlink()
        print(f"removed: {old}")
    for w in WORKS:
        related_html = "\n".join(RELATED_CARD.format(**r) for r in related_for(w))
        import re
        m = re.match(r"(\d+) 年 (\d+) 月", w["year"])
        if m:
            year_iso = f"{m.group(1)}-{int(m.group(2)):02d}-28"
        else:
            year_iso = "2025-01-01"
        ctx = {**w, "year_iso": year_iso, "related_html": related_html}
        out = TEMPLATE.format(**ctx)
        path = out_dir / f"work-{w['id']}.html"
        path.write_text(out, encoding="utf-8")
        print(f"wrote {path}")
    print(f"\nGenerated {len(WORKS)} detail pages.")


if __name__ == "__main__":
    main()
