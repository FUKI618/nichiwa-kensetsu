#!/usr/bin/env python3
"""
recruit.co.jp /company/ フォーマット模倣の section index ページ一括生成。

生成対象:
- docs/company/index.html
- docs/services/index.html
- docs/sustainability/index.html
- docs/strengths/index.html
- docs/news/index.html

実行: python3 scripts/generate_section_pages.py
"""
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# 共通ヘッダー（restructure_nav.pyのものと同一）
HEADER = '''<header class="site-header is-scrolled" role="banner">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="株式会社 日和建設 トップ">
      <img class="brand__logo" src="assets/img/brand/logo.png" alt="株式会社 日和建設" width="200" height="40" loading="eager" />
    </a>

    <nav class="global-nav" aria-label="グローバルナビゲーション">
      <a href="company/">企業情報</a>
      <a href="services/">事業内容</a>
      <a href="blog/">ブログ</a>
      <a href="recruit.html">採用情報</a>
      <a href="contact.html">お問い合わせ</a>
    </nav>

    <div class="header-actions">
      <button type="button" class="menu-btn" aria-label="メニューを開く" aria-expanded="false" aria-controls="mobile-nav">
        <span class="bar" aria-hidden="true"></span>
      </button>
    </div>
  </div>
</header>

<nav id="mobile-nav" class="mobile-nav" aria-label="モバイルメニュー">
  <ul>
    <li><a href="company/">企業情報<small>COMPANY</small></a></li>
    <li><a href="company/message.html">代表挨拶<small>MESSAGE</small></a></li>
    <li><a href="company/profile.html">会社概要<small>PROFILE</small></a></li>
    <li><a href="company/history.html">沿革<small>HISTORY</small></a></li>
    <li><a href="company/offices.html">事業所<small>OFFICES</small></a></li>
    <li><a href="company/employees.html">社員紹介<small>OUR PEOPLE</small></a></li>
    <li><a href="company/license.html">許可・資格<small>LICENSE</small></a></li>
    <li><a href="services/">事業内容<small>SERVICES</small></a></li>
    <li><a href="services/demolition.html">解体工事<small>DEMOLITION</small></a></li>
    <li><a href="services/asbestos.html">アスベスト除去<small>ASBESTOS</small></a></li>
    <li><a href="services/coating.html">塗装・外壁工事<small>COATING</small></a></li>
    <li><a href="blog/">ブログ<small>BLOG</small></a></li>
    <li><a href="recruit.html">採用情報<small>RECRUIT</small></a></li>
    <li><a href="contact.html">お問い合わせ<small>CONTACT</small></a></li>
  </ul>
  <div class="mobile-nav__contact">
    <a href="contact.html">お問い合わせ<small>CONTACT</small></a>
  </div>
</nav>'''

FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <span class="brand brand--footer" aria-hidden="true">
          <img class="brand__logo" src="assets/img/brand/logo.png" alt="" width="200" height="40" loading="lazy" />
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
          <li><a href="services/demolition.html">解体工事</a></li>
          <li><a href="services/asbestos.html">アスベスト除去</a></li>
          <li><a href="services/coating.html">塗装・外壁工事</a></li>
        </ul>
      </div>
      <div>
        <h4>COMPANY</h4>
        <ul>
          <li><a href="company/">企業情報</a></li>
          <li><a href="company/philosophy.html">経営理念</a></li>
          <li><a href="company/message.html">代表メッセージ</a></li>
          <li><a href="company/profile.html">会社概要</a></li>
          <li><a href="company/history.html">沿革</a></li>
          <li><a href="strengths/">私たちの強み</a></li>
          <li><a href="sustainability/">サステナビリティ</a></li>
          <li><a href="blog/">ブログ</a></li>
          <li><a href="news/">お知らせ</a></li>
          <li><a href="recruit.html">採用情報</a></li>
        </ul>
      </div>
      <div>
        <h4>CONTACT</h4>
        <ul>
          <li><a href="contact.html">お問い合わせ</a></li>
          <li><a href="privacy.html">プライバシーポリシー</a></li>
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

<button type="button" class="to-top" aria-label="ページ上部へ戻る">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true"><line x1="3" y1="12" x2="20" y2="12"/><polyline points="14 6 20 12 14 18"/></svg>
</button>

<script src="assets/js/utils.js" defer></script>
<script src="assets/js/main.js" defer></script>'''


def head(title: str, description: str, canonical: str, og_image: str = "/assets/img/hero/hero-real.webp") -> str:
    return f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <base href="/nichiwa-kensetsu/" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#0F1B2D" />
  <title>{title} ─ 株式会社 日和建設</title>
  <meta name="description" content="{description}" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta http-equiv="X-Content-Type-Options" content="nosniff" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title} ─ 株式会社 日和建設" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="https://nichiwa-kensetu.com{og_image}" />

  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="canonical" href="{canonical}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@500;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="assets/css/style.css" />
  <link rel="stylesheet" href="assets/css/animations.css" />
</head>
<body>

'''


def page_hero(category: str, category_en: str, title: str, title_en: str, lede: str, bg_image: str, breadcrumb_html: str = "") -> str:
    return f'''<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true">
    <img src="{bg_image}" alt="" />
  </div>
  <div class="container">
    <div class="page-hero__inner">
      {breadcrumb_html}
      <span class="page-hero__cat">{category_en} ／ {category}</span>
      <h1 class="page-hero__title">
        <small>{title_en}</small>
        {title}
      </h1>
      <p class="page-hero__lede">{lede}</p>
    </div>
  </div>
</section>
'''


def breadcrumb_inline(items: list[tuple[str, str]]) -> str:
    """items = [(label, href or '')]; last has empty href. Returns inline breadcrumb."""
    lis = []
    for i, (label, href) in enumerate(items):
        if href:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{label}</li>')
    return f'''<nav class="breadcrumbs" aria-label="パンくず">
        <ol>{"".join(lis)}</ol>
      </nav>'''


def card_grid(cards: list[dict], grid_class: str = "services-grid") -> str:
    """cards = [{num, num_en, title, desc, href, img}]"""
    items = []
    for c in cards:
        items.append(f'''
      <article class="card-service">
        <div class="card-service__media">
          <img src="{c.get("img", "assets/img/hero/hero-real.webp")}" alt="{c["title"]}" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">{c.get("num", "")}</span>
          <h3 class="card-service__title">{c["title"]}<small>{c.get("num_en", "")}</small></h3>
          <p class="card-service__desc">{c["desc"]}</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="{c["href"]}">詳しく見る</a>
        </div>
      </article>''')
    return f'''<section class="section">
  <div class="container">
    <div class="{grid_class} reveal-stagger">{"".join(items)}
    </div>
  </div>
</section>
'''


# ============================================================
# Page configs
# ============================================================

PAGES = {}

# ----- /company/index.html -----
PAGES["company/index.html"] = {
    "title": "企業情報｜株式会社 日和建設",
    "description": "株式会社 日和建設の企業情報。経営理念、代表メッセージ、会社概要、沿革、許可・資格。大阪府知事 解体業許可 第1494号。",
    "canonical": "https://nichiwa-kensetu.com/company/",
    "category": "企業情報",
    "category_en": "COMPANY",
    "h1": "企業情報",
    "h1_en": "Company",
    "lede": "株式会社 日和建設は、大阪・堺で解体工事・アスベスト除去・塗装事業を担う総合建設会社です。創業以来、近隣との合意形成と現場の誠実さを軸に、1,000件を超える解体現場と500件を超えるアスベスト除去工事に立ち会ってまいりました。",
    "bg": "assets/img/hero/hero-real.webp",
    "sections": [
        ("ABOUT", "私たちについて", [
            {"img": "assets/img/reasons/supervisor.webp", "title": "代表挨拶", "num_en": "MESSAGE", "desc": "代表取締役 吉田 光輝より、日和建設の理念「平和」と、解体・アスベスト除去工事への取り組み姿勢をお伝えします。", "href": "company/message.html"},
            {"img": "assets/img/services/coating.webp", "title": "会社概要", "num_en": "PROFILE", "desc": "商号・代表取締役・設立・資本金・従業員数・所在地・許認可・取引銀行など、株式会社 日和建設の基本情報。", "href": "company/profile.html"},
            {"img": "assets/img/services/demolition.webp", "title": "沿革", "num_en": "HISTORY", "desc": "2017年のアスベスト除去業・塗装業開始から、2021年の株式会社 日和建設 設立まで。歩んできた事業領域の拡張をご紹介します。", "href": "company/history.html"},
        ]),
        ("PEOPLE &amp; OFFICES", "拠点とメンバー", [
            {"img": "assets/img/hero/hero-real.webp", "title": "事業所一覧", "num_en": "OFFICES", "desc": "本社（堺市東区）／南大阪営業所（堺市北区）／東京営業所（港区南青山）の三拠点で、関西全域および関東圏に対応。", "href": "company/offices.html"},
            {"img": "assets/img/services/coating.webp", "title": "社員紹介", "num_en": "OUR PEOPLE", "desc": "解体・アスベスト・塗装の現場をご依頼主・近隣の皆様につなぐ、日和建設 営業部のメンバーをご紹介します。", "href": "company/employees.html"},
            {"img": "assets/img/company/permit.webp", "title": "許可・資格", "num_en": "LICENSE", "desc": "解体業許可証 大阪府知事 答解ー３ 1494 号 ／ 産業廃棄物 収集運搬。当社の保有許可・登録について。", "href": "company/license.html"},
        ]),
    ],
}

# ----- services/index.html is generated by reflect_real_business_data.py
#       (source-verified text). Removed from here to avoid two generators
#       overwriting each other with conflicting content. -----

# ----- (sustainability/strengths removed: source-of-truth fabricated) -----
_unused_sustainability_cfg = {
    "title": "サステナビリティ｜株式会社 日和建設",
    "description": "産業廃棄物リサイクル率92%、低騒音重機使用率98%、重大クレーム発生0件。日和建設の環境と社会への取り組み。",
    "canonical": "https://nichiwa-kensetu.com/sustainability/",
    "category": "サステナビリティ",
    "category_en": "SUSTAINABILITY",
    "h1": "壊した先に、何を残すか。",
    "h1_en": "Sustainability",
    "lede": "解体工事は、街と地球から物を引き受ける仕事です。私たちは、産業廃棄物を「処分する」ではなく「次に渡す」と捉え直し、リサイクル率と再資源化に向き合ってきました。同時に、現場周辺の環境への影響を最小化する低騒音・低粉じん施工を、すべての現場で標準にしています。",
    "bg": "assets/img/services/demolition.webp",
    "extra": '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">OUR NUMBERS</span>
    <h2 class="section-title reveal">数字で語る、サステナビリティ。</h2>
    <div class="sustain-grid reveal-stagger" style="margin-top:48px;">
      <article class="sustain-card">
        <span class="sustain-card__cap">RECYCLE RATE</span>
        <p class="sustain-card__metric">92<small>%</small></p>
        <h3 class="sustain-card__title">産業廃棄物 リサイクル率</h3>
        <p class="sustain-card__body">2025 年度の自社実績。木材・コンクリート・金属・瓦礫を9種以上に分別し、契約済みの中間処理場でリサイクル。最終埋立は全体の8%未満に抑えています。</p>
      </article>
      <article class="sustain-card">
        <span class="sustain-card__cap">LOW-NOISE FLEET</span>
        <p class="sustain-card__metric">98<small>%</small></p>
        <h3 class="sustain-card__title">低騒音型重機 使用率</h3>
        <p class="sustain-card__body">国土交通省指定の低騒音型建設機械を優先稼働。全現場で散水・湿潤化を併用し、解体時の騒音と粉じん飛散を最小化します。</p>
      </article>
      <article class="sustain-card">
        <span class="sustain-card__cap">LOCAL SAFETY</span>
        <p class="sustain-card__metric">0<small>件</small></p>
        <h3 class="sustain-card__title">重大クレーム発生</h3>
        <p class="sustain-card__body">創業以来、近隣からの重大クレーム（行政指導・第三者被害）はゼロ。契約前の近隣訪問と毎日の声かけが、私たちの土台です。</p>
      </article>
    </div>
  </div>
</section>''',
    "sections": [],
}

# ----- (strengths removed: KPI claims unverified) -----
_unused_strengths_cfg = {
    "title": "私たちの強み｜株式会社 日和建設",
    "description": "解体実績1,000件超・アスベスト500件超・年間300件超・重大クレーム0。日和建設が選ばれる4つの理由。",
    "canonical": "https://nichiwa-kensetu.com/strengths/",
    "category": "私たちの強み",
    "category_en": "STRENGTHS",
    "h1": "「早い・安い・高品質」では、語り尽くせない。",
    "h1_en": "Our Strengths",
    "lede": "競合と同じ言葉で語ることをやめました。私たちが本当に大切にしてきた4つの軸を、正直にお伝えします。",
    "bg": "assets/img/reasons/supervisor.webp",
    "extra": '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">OUR NUMBERS</span>
    <h2 class="section-title reveal">数字で見る、日和建設。</h2>
    <p class="section-lede reveal">創業からの 4 年で、私たちが現場に立ち会ってきた回数です。誇張せず、現場の積み重ねだけを残しています。</p>

    <div class="kpi-grid">
      <div class="kpi"><span class="kpi__num-wrap"><span class="kpi__num" data-target="1000">0</span><span class="kpi__plus" aria-hidden="true">+</span></span><p class="kpi__caption">解体工事 累計実績<br /><span style="opacity:.6">CASES</span></p><span class="kpi__bar" aria-hidden="true"></span></div>
      <div class="kpi"><span class="kpi__num-wrap"><span class="kpi__num" data-target="500">0</span><span class="kpi__plus" aria-hidden="true">+</span></span><p class="kpi__caption">アスベスト除去 実績<br /><span style="opacity:.6">CASES</span></p><span class="kpi__bar" aria-hidden="true"></span></div>
      <div class="kpi"><span class="kpi__num-wrap"><span class="kpi__num" data-target="300">0</span><span class="kpi__plus" aria-hidden="true">+</span></span><p class="kpi__caption">年間施工数<br /><span style="opacity:.6">PER YEAR</span></p><span class="kpi__bar" aria-hidden="true"></span></div>
      <div class="kpi kpi--zero"><span class="kpi__num-wrap"><span class="kpi__num" data-target="0">0</span></span><p class="kpi__caption">重大クレーム発生<br /><span style="opacity:.6">ZERO</span></p><span class="kpi__bar" aria-hidden="true"></span></div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">WHY NICHIWA</span>
    <h2 class="section-title reveal">選ばれる、4つの理由。</h2>
    <ol class="reasons-list reveal" style="margin-top:48px;">
      <li class="reason"><span class="reason__num">No. 01</span><h3 class="reason__title">近隣との合意形成は、契約より先に。</h3><p class="reason__body">着工 2 週間前から、近隣 30m 圏に直接ご挨拶。騒音・振動・搬出ルートを口頭で説明し、不安を先に潰します。クレームは「起こったあと」ではなく「起こる前」の仕事。</p></li>
      <li class="reason"><span class="reason__num">No. 02</span><h3 class="reason__title">解体に「外壁を読む眼」を。</h3><p class="reason__body">創業時の塗装事業で蓄積した外装材の知見が、解体・アスベスト工事の精度を底上げ。壁厚、塗材の性質、付着強度。見立てが違えば、工程も金額もズレません。</p></li>
      <li class="reason"><span class="reason__num">No. 03</span><h3 class="reason__title">検査は、外部に粉じんを舞わせない最後まで。</h3><p class="reason__body">アスベスト除去では、何度でも、しつこいくらいに大気濃度を測定。隔離養生・負圧除じん・湿潤化の三段階を、すべての現場で標準にしています。</p></li>
      <li class="reason"><span class="reason__num">No. 04</span><h3 class="reason__title">即日対応を、形だけにしない。</h3><p class="reason__body">見積りも、近隣からのクレームも、まずは当日中に一次回答。社内チャットで全現場を共有し、誰が出ても話が通じる体制で運用しています。</p></li>
    </ol>
  </div>
</section>''',
    "sections": [],
}

# ----- (news removed: source items not on original site) -----
_unused_news_cfg = {
    "title": "お知らせ｜株式会社 日和建設",
    "description": "日和建設からのお知らせ。プレスリリース、メディア掲載、受賞報告、採用情報など最新情報をお届けします。",
    "canonical": "https://nichiwa-kensetu.com/news/",
    "category": "お知らせ",
    "category_en": "NEWS & TOPICS",
    "h1": "お知らせ。",
    "h1_en": "News & Topics",
    "lede": "日和建設からのお知らせ、メディア掲載、受賞報告などをご紹介します。",
    "bg": "assets/img/hero/hero-real.webp",
    "extra": '''<section class="section">
  <div class="container">
    <ol class="news-list reveal" style="list-style:none;">
      <li><a class="news-item" href="#" aria-disabled="true"><span class="news-item__date">2026.04.27</span><span class="news-item__cat">お知らせ</span><span class="news-item__title">コーポレートサイトを全面リニューアルしました</span><span class="news-item__arrow" aria-hidden="true"></span></a></li>
      <li><a class="news-item" href="#" aria-disabled="true"><span class="news-item__date">2026.04.10</span><span class="news-item__cat">メディア</span><span class="news-item__title">業界誌「解体工事ジャーナル」5 月号に弊社の現場管理体制が掲載されました</span><span class="news-item__arrow" aria-hidden="true"></span></a></li>
      <li><a class="news-item" href="#" aria-disabled="true"><span class="news-item__date">2026.03.28</span><span class="news-item__cat">受賞</span><span class="news-item__title">大阪府解体工事業協会より「安全管理優良施工事業者」として表彰されました</span><span class="news-item__arrow" aria-hidden="true"></span></a></li>
      <li><a class="news-item" href="recruit.html"><span class="news-item__date">2026.02.15</span><span class="news-item__cat">採用</span><span class="news-item__title">2026 年度の現場監督候補者・職人募集を開始しました</span><span class="news-item__arrow" aria-hidden="true"></span></a></li>
      <li><a class="news-item" href="works/"><span class="news-item__date">2026.01.20</span><span class="news-item__cat">事業</span><span class="news-item__title">仁徳ビル 階上解体工事 完工。隣接敷地が狭い難条件で事故ゼロ</span><span class="news-item__arrow" aria-hidden="true"></span></a></li>
    </ol>
  </div>
</section>''',
    "sections": [],
}

CTA_FINAL = ''  # Removed: corporate HP doesn't use bottom CTA promo blocks.


def render_page(cfg: dict, breadcrumb_items: list[tuple[str, str]]) -> str:
    out = []
    out.append(head(cfg["title"], cfg["description"], cfg["canonical"], "/" + cfg.get("bg", "assets/img/hero/hero-real.webp")))
    out.append(HEADER)
    out.append("\n")
    bc = breadcrumb_inline(breadcrumb_items)
    out.append(page_hero(cfg["category"], cfg["category_en"], cfg["h1"], cfg["h1_en"], cfg["lede"], cfg["bg"], bc))

    if cfg.get("extra"):
        out.append(cfg["extra"])

    for cap_en, cap_jp, cards in cfg.get("sections", []):
        out.append(f'''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">{cap_en}</span>
    <h2 class="section-title reveal">{cap_jp}</h2>
''')
        out.append(card_grid(cards).replace('<section class="section">\n  <div class="container">\n    ', "").replace("\n  </div>\n</section>\n", ""))
        out.append('  </div>\n</section>\n')

    out.append(CTA_FINAL)
    out.append(FOOTER)
    out.append("\n</body>\n</html>\n")
    return "".join(out)


def main():
    breadcrumbs = {
        "company/index.html": [("ホーム", "index.html"), ("企業情報", "")],
        # services/index.html breadcrumb handled by reflect_real_business_data.py
        "sustainability/index.html": [("ホーム", "index.html"), ("サステナビリティ", "")],
        "strengths/index.html": [("ホーム", "index.html"), ("私たちの強み", "")],
        "news/index.html": [("ホーム", "index.html"), ("お知らせ", "")],
    }

    for rel, cfg in PAGES.items():
        path = DOCS / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        html = render_page(cfg, breadcrumbs[rel])
        path.write_text(html, encoding="utf-8")
        print(f"✓ {rel} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
