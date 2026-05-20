#!/usr/bin/env python3
"""
nichiwa-kensetu.com から取得した実データで全ページを再構築。
架空のKPI/役員/Blog 記事/4本柱 は全削除済み。
このスクリプトは残ったページに本物のテキストを流し込む。

出力対象:
- docs/company/message.html       元サイトの「平和」哲学CEOメッセージ
- docs/company/profile.html       3拠点実住所・取引銀行・実事業内容
- docs/company/history.html       実沿革 2017→2021
- docs/company/offices.html       実3拠点
- docs/company/employees.html     実3名 (NEW)
- docs/company/index.html         landing 再設計
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline, CTA_FINAL, card_grid

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# ============================================================
# CEO MESSAGE — TOPページコピー + 元サイト本文をミックスして再構成
# ヘッダー画像は人物ではなく業種（解体現場）の cinematic 風景
# ============================================================
MESSAGE_BODY = '''<section class="section section--navy">
  <div class="container">
    <div style="max-width:760px; margin: 0 auto;">
      <span class="ceo-message__caption reveal" style="display:block; margin-bottom:24px;">MESSAGE FROM CEO</span>
      <h2 class="ceo-message__title reveal" style="font-family:var(--ff-serif-jp); font-weight:700; font-size:clamp(28px, 3.4vw, 44px); line-height:1.65; letter-spacing:.04em; margin-bottom:56px;">街の節目に、<br />立ち会う仕事を。</h2>

      <div class="ceo-message__body reveal" style="font-size:15.5px; line-height:2.3; letter-spacing:.03em; color: rgba(250,250,247,.92);">
        <p style="margin-bottom:24px;">数あるホームページの中から、株式会社 日和建設をご覧いただき、ありがとうございます。</p>

        <p style="margin-bottom:24px;">私たちが向き合っているのは、街の「節目」です。古い建物の最後の一日と、次の街の最初の一日が出会う、その境目に立ち会うのが、解体・アスベスト除去・塗装という仕事です。</p>

        <p style="margin-bottom:24px;">日和建設は創業以来、外壁リフォームに始まり、解体工事、アスベスト除去工事へと、お客様の声に応えながら事業を広げてまいりました。日本に生まれ、日本で商いをさせていただいている人間として、私たちが掲げている理念があります。</p>

        <p style="margin: 40px 0; font-family:var(--ff-serif-jp); font-size:28px; font-weight:600; color: var(--c-brass); letter-spacing:.08em; text-align:center;">それは、「平和」です。</p>

        <p style="margin-bottom:24px;">解体工事、アスベスト除去工事に対するイメージは、長らく不評ばかりでした。だからこそ私たちは、コンプライアンスと社会的マナーの教育に力を入れて取り組んでいます。挨拶を欠かさない、環境への配慮を忘れない ── そうした当たり前を、当たり前にできる組織にすること。それが私の第一の目標です。</p>

        <p style="margin-bottom:24px;">解体工事のイメージを、クリーンに変えていきたい。騙し合い、いじめ、環境破壊、近隣への迷惑 ── そういったものから無縁の、平和な事業へ。小さな会社ながらも、業界に少しでも影響を与えていけるよう、日々鍛錬を続けてまいります。私たちのような若手がしっかりしないと、今の日本は変えられない。何事にも、その責任感を持って行動してまいります。</p>

        <p style="margin-bottom:24px;">いい環境を、笑顔をお届けできるよう、現場・お客様・近隣の皆様と協力し合いながら、これからも仕事に取り組んでまいります。</p>
      </div>

      <div class="ceo-message__sign reveal" style="margin-top:56px; padding-top:32px; border-top:1px solid var(--c-line-dark); text-align:right;">
        <span style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); display:block; margin-bottom:8px;">代表取締役</span>
        <span style="font-family:var(--ff-serif-jp); font-size:22px; font-weight:600; letter-spacing:.08em;">吉田 光輝</span>
      </div>
    </div>
  </div>
</section>
'''

# ============================================================
# PROFILE — 実データ
# ============================================================
PROFILE_BODY = '''<section class="section section--navy">
  <div class="container">
    <span class="eyebrow reveal">COMPANY PROFILE</span>
    <h2 class="section-title reveal">会社概要。</h2>

    <div class="company-layout" style="margin-top:48px;">
      <div class="reveal">
        <table class="company-table">
          <tbody>
            <tr><th>会社名</th><td>株式会社 日和建設</td></tr>
            <tr><th>代表取締役</th><td>吉田 光輝</td></tr>
            <tr><th>設立</th><td>2021年 7月 2日</td></tr>
            <tr><th>資本金</th><td>500 万円</td></tr>
            <tr><th>事業内容</th><td>建設業、不動産業、建築業</td></tr>
            <tr><th>従業員数</th><td>30 名</td></tr>
            <tr><th>取引銀行</th><td>関西みらい銀行 ／ 三菱 UFJ 銀行 ／ 三井住友銀行</td></tr>
            <tr><th>本社</th><td>〒599-8126<br />大阪府堺市東区大美野 171-36</td></tr>
            <tr><th>南大阪営業所</th><td>〒591-8032<br />大阪府堺市北区百舌鳥梅町 3-6-1</td></tr>
            <tr><th>東京営業所</th><td>〒107-0062<br />東京都港区南青山 2-2-15<br />win青山 531</td></tr>
            <tr><th>TEL</th><td><a href="tel:0722390126" style="color:var(--c-brass);">072-239-0126</a></td></tr>
            <tr><th>FAX</th><td>072-236-6491</td></tr>
            <tr><th>MAIL</th><td><a href="mailto:info@nichiwa-kensetu.com" style="color:var(--c-brass);">info@nichiwa-kensetu.com</a></td></tr>
            <tr><th>許可・登録</th><td>解体業許可証 大阪府知事 答解ー３ 1494 号<br />産業廃棄物 収集運搬</td></tr>
          </tbody>
        </table>
      </div>

      <aside class="company-aside reveal">
        <img src="assets/img/company/permit.webp" alt="解体業許可証イメージ" width="720" height="900" loading="lazy" />
      </aside>
    </div>
  </div>
</section>
'''

# ============================================================
# HISTORY — 実沿革
# ============================================================
HISTORY_BODY = '''<section class="history">
  <div class="container">
    <span class="eyebrow reveal">HISTORY</span>
    <h2 class="section-title reveal">これまでの歩み。</h2>
    <p class="section-lede reveal">外壁リフォームから始まり、塗装・アスベスト除去・解体・内装・設備まで。一歩ずつ事業領域を広げ、2021年に株式会社 日和建設として法人化しました。</p>

    <ol class="timeline-history reveal">
      <li>
        <span class="timeline-history__year">2017.02</span>
        <div>
          <h3 class="timeline-history__title">アスベスト除去業・塗装業 開始</h3>
          <p class="timeline-history__body">マンション、一般住宅などの請負工事を主に活動を始める。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2019.01</span>
        <div>
          <h3 class="timeline-history__title">営業部 発足</h3>
          <p class="timeline-history__body">専任の営業体制を立ち上げ、案件管理と顧客折衝の精度を高める。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2019.02</span>
        <div>
          <h3 class="timeline-history__title">解体工事業 開始</h3>
          <p class="timeline-history__body">外壁・塗装で培った建物への眼を活かし、解体工事業へ事業領域を拡張。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2019.04</span>
        <div>
          <h3 class="timeline-history__title">外壁工事 一式対応へ</h3>
          <p class="timeline-history__body">塗装工事から外壁工事一式として、足場工事、防水工事、シール工事、外壁補修工事などを主に請け負うようになる。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2020.01</span>
        <div>
          <h3 class="timeline-history__title">内装・設備・水道 領域へ</h3>
          <p class="timeline-history__body">内装工事、設備関係、水道関係の活動を始める。建物の一生に幅広く関わる体制へ。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2021.07</span>
        <div>
          <h3 class="timeline-history__title">株式会社 日和建設 設立</h3>
          <p class="timeline-history__body">大阪府堺市東区大美野にて法人化。資本金 500 万円。代表取締役 吉田 光輝。</p>
        </div>
      </li>
    </ol>
  </div>
</section>
'''

# ============================================================
# OFFICES — 実3拠点
# ============================================================
OFFICES_BODY = '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">OUR OFFICES</span>
    <h2 class="section-title reveal">三拠点で、関西と関東を。</h2>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">No. 01 ／ HQ</span>
          <h3 class="card-service__title">本社<small>HEADQUARTERS — SAKAI</small></h3>
          <p class="card-service__desc" style="line-height:2.2;">
            〒599-8126<br />
            大阪府堺市東区大美野 171-36<br /><br />
            TEL <a href="tel:0722390126" style="color:var(--c-brass);">072-239-0126</a><br />
            FAX 072-236-6491
          </p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">No. 02 ／ MINAMI-OSAKA</span>
          <h3 class="card-service__title">南大阪営業所<small>SOUTH OSAKA BRANCH</small></h3>
          <p class="card-service__desc" style="line-height:2.2;">
            〒591-8032<br />
            大阪府堺市北区百舌鳥梅町 3-6-1
          </p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">No. 03 ／ TOKYO</span>
          <h3 class="card-service__title">東京営業所<small>TOKYO BRANCH</small></h3>
          <p class="card-service__desc" style="line-height:2.2;">
            〒107-0062<br />
            東京都港区南青山 2-2-15<br />
            win青山 531
          </p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
    </div>
  </div>
</section>
'''

# ============================================================
# EMPLOYEES (NEW) — 実3名
# ============================================================
EMPLOYEES_BODY = '''<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">OUR PEOPLE</span>
    <h2 class="section-title reveal">日和建設の、営業メンバー。</h2>
    <p class="section-lede reveal">解体・アスベスト・塗装の現場をご依頼主・近隣の皆様につなぐ、営業部のメンバーをご紹介します。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">SALES</span>
          <h3 class="card-service__title">前田 凌<small>RYO MAEDA ／ 営業部</small></h3>
          <p class="card-service__desc">弊社に入社し、まだまだ勉強中の身ではありますが、【仕事】とは何か、常に先のことを考え予測し、人との繋がりの難しさを実感いたしました。その経験を生かし、お客様・先方様に少しでもお力になりたいと考えております。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">SALES</span>
          <h3 class="card-service__title">伊藤 康文<small>YASUFUMI ITO ／ 営業部</small></h3>
          <p class="card-service__desc">お客様への価値のご提供と、日和建設に解体工事・アスベスト除去工事などの工事をご依頼いただいて「よかった」と言っていただけるように、日々営業活動に全力投球しています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">SALES</span>
          <h3 class="card-service__title">日極 周英<small>SHUEI HIGOKI ／ 営業部</small></h3>
          <p class="card-service__desc">関係者の方、お客様、全員に喜んでもらえるよう、努力を絶やしません。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
    </div>
  </div>
</section>
'''


PAGES = {
    "company/message.html": {
        "title": "代表挨拶｜株式会社 日和建設",
        "description": "代表取締役 吉田 光輝より。日和建設の理念は「平和」── 街の節目に立ち会う仕事として、解体・アスベスト除去・塗装に誠実に取り組んでいます。",
        "canonical": "https://nichiwa-kensetu.com/company/message.html",
        "category": "代表挨拶",
        "category_en": "MESSAGE",
        "h1": "街の節目に、<br />立ち会う仕事を。",
        "h1_en": "Message from CEO",
        "lede": "建物の最後の一日から、次の街の最初の一日まで ── 解体・アスベスト除去・塗装を通じて、街の節目に立ち会うのが、私たちの仕事です。",
        "bg": "assets/img/message/message-hero.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("代表挨拶", "")],
        "body": MESSAGE_BODY,
    },
    "company/profile.html": {
        "title": "会社概要｜株式会社 日和建設",
        "description": "株式会社 日和建設の会社概要。代表取締役 吉田 光輝、設立2021年7月、資本金500万円、従業員30名。本社（堺市東区）／南大阪営業所／東京営業所の三拠点体制。",
        "canonical": "https://nichiwa-kensetu.com/company/profile.html",
        "category": "会社概要",
        "category_en": "PROFILE",
        "h1": "会社概要。",
        "h1_en": "Company Profile",
        "lede": "株式会社 日和建設の基本情報。設立、所在地、許認可、取引銀行など。",
        "bg": "assets/img/services/coating.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("会社概要", "")],
        "body": PROFILE_BODY,
    },
    "company/history.html": {
        "title": "沿革｜株式会社 日和建設",
        "description": "2017年のアスベスト除去業・塗装業開始から、解体工事業、外壁工事一式、内装・設備、そして2021年の法人化まで。日和建設のこれまでの歩み。",
        "canonical": "https://nichiwa-kensetu.com/company/history.html",
        "category": "沿革",
        "category_en": "HISTORY",
        "h1": "これまでの歩み。",
        "h1_en": "Our History",
        "lede": "2017年のアスベスト除去業・塗装業の開始から、2021年の株式会社 日和建設 設立まで。事業領域を一歩ずつ広げてきた歩みです。",
        "bg": "assets/img/services/demolition.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("沿革", "")],
        "body": HISTORY_BODY,
    },
    "company/offices.html": {
        "title": "事業所一覧｜株式会社 日和建設",
        "description": "本社（大阪府堺市東区大美野）／南大阪営業所（堺市北区百舌鳥梅町）／東京営業所（東京都港区南青山）の三拠点で関西全域および関東圏に対応。",
        "canonical": "https://nichiwa-kensetu.com/company/offices.html",
        "category": "事業所一覧",
        "category_en": "OFFICES",
        "h1": "三拠点で、関西と関東を。",
        "h1_en": "Offices",
        "lede": "本社（堺）／南大阪営業所／東京営業所の三拠点体制で、関西全域および関東圏の解体・アスベスト除去・塗装工事に対応しています。",
        "bg": "assets/img/hero/hero-real.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("事業所一覧", "")],
        "body": OFFICES_BODY,
    },
    "company/employees.html": {
        "title": "社員紹介｜株式会社 日和建設",
        "description": "日和建設 営業部のメンバー紹介。前田 凌、伊藤 康文、日極 周英 ── お客様と現場をつなぐ営業チームの3名。",
        "canonical": "https://nichiwa-kensetu.com/company/employees.html",
        "category": "社員紹介",
        "category_en": "OUR PEOPLE",
        "h1": "営業メンバー。",
        "h1_en": "Our People",
        "lede": "解体・アスベスト・塗装の現場をご依頼主・近隣の皆様につなぐ、日和建設 営業部のメンバーをご紹介します。",
        "bg": "assets/img/services/coating.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("社員紹介", "")],
        "body": EMPLOYEES_BODY,
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
        html += CTA_FINAL
        html += FOOTER
        html += "\n</body>\n</html>\n"
        path.write_text(html, encoding="utf-8")
        print(f"✓ {rel} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
