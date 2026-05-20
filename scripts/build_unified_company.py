#!/usr/bin/env python3
"""
/company/ を 6サブページ統合の単一ページとして再構築。

旧構成:
  /company/index.html  → 6カードグリッド (each links to sub)
  /company/message.html
  /company/profile.html
  /company/history.html
  /company/offices.html
  /company/employees.html
  /company/license.html

新構成:
  /company/index.html  → 全コンテンツを縦長セクションで一画面に
  ── サブページは削除（同じ内容は /company/#anchor で参照可）
  ── ホームから1クリックで全部見える設計

実行: python3 scripts/build_unified_company.py
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "company" / "index.html"

# ============================================================
# Section 1: 代表挨拶
# ============================================================
MESSAGE_SECTION = '''<section id="message" class="section section--navy">
  <div class="container">
    <span class="eyebrow reveal">MESSAGE</span>
    <h2 class="section-title reveal" style="margin-bottom:48px;">代表挨拶。</h2>

    <div style="max-width:760px; margin: 0 auto;">
      <h3 class="reveal" style="font-family:var(--ff-serif-jp); font-weight:700; font-size:clamp(26px, 3vw, 38px); line-height:1.7; letter-spacing:.04em; margin-bottom:48px;">街の節目に、<br />立ち会う仕事を。</h3>

      <div class="reveal" style="font-size:15.5px; line-height:2.3; letter-spacing:.03em; color: rgba(250,250,247,.92);">
        <p style="margin-bottom:24px;">数あるホームページの中から、株式会社 日和建設をご覧いただき、ありがとうございます。</p>
        <p style="margin-bottom:24px;">私たちが向き合っているのは、街の「節目」です。古い建物の最後の一日と、次の街の最初の一日が出会う、その境目に立ち会うのが、解体・アスベスト除去・塗装という仕事です。</p>
        <p style="margin-bottom:24px;">日和建設は創業以来、外壁リフォームに始まり、解体工事、アスベスト除去工事へと、お客様の声に応えながら事業を広げてまいりました。日本に生まれ、日本で商いをさせていただいている人間として、私たちが掲げている理念があります。</p>
        <p style="margin: 40px 0; font-family:var(--ff-serif-jp); font-size:28px; font-weight:600; color: var(--c-brass); letter-spacing:.08em; text-align:center;">それは、「平和」です。</p>
        <p style="margin-bottom:24px;">解体工事、アスベスト除去工事に対するイメージは、長らく不評ばかりでした。だからこそ私たちは、コンプライアンスと社会的マナーの教育に力を入れて取り組んでいます。挨拶を欠かさない、環境への配慮を忘れない ── そうした当たり前を、当たり前にできる組織にすること。それが私の第一の目標です。</p>
        <p style="margin-bottom:24px;">解体工事のイメージを、クリーンに変えていきたい。騙し合い、いじめ、環境破壊、近隣への迷惑 ── そういったものから無縁の、平和な事業へ。小さな会社ながらも、業界に少しでも影響を与えていけるよう、日々鍛錬を続けてまいります。私たちのような若手がしっかりしないと、今の日本は変えられない。何事にも、その責任感を持って行動してまいります。</p>
        <p>いい環境を、笑顔をお届けできるよう、現場・お客様・近隣の皆様と協力し合いながら、これからも仕事に取り組んでまいります。</p>
      </div>

      <div class="reveal" style="margin-top:56px; padding-top:32px; border-top:1px solid var(--c-line-dark); text-align:right;">
        <span style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); display:block; margin-bottom:8px;">代表取締役</span>
        <span style="font-family:var(--ff-serif-jp); font-size:22px; font-weight:600; letter-spacing:.08em;">吉田 光輝</span>
      </div>
    </div>
  </div>
</section>
'''

# ============================================================
# Section 2: 会社概要
# ============================================================
PROFILE_SECTION = '''<section id="profile" class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">PROFILE</span>
    <h2 class="section-title reveal" style="margin-bottom:48px;">会社概要。</h2>

    <div style="max-width:880px; margin: 0 auto;">
      <table class="company-table" style="width:100%;">
        <tbody>
          <tr><th>会社名</th><td>株式会社 日和建設</td></tr>
          <tr><th>代表取締役</th><td>吉田 光輝</td></tr>
          <tr><th>設立</th><td>2021年 7月 2日</td></tr>
          <tr><th>資本金</th><td>500 万円</td></tr>
          <tr><th>事業内容</th><td>建設業、不動産業、建築業</td></tr>
          <tr><th>従業員数</th><td>30 名</td></tr>
          <tr><th>取引銀行</th><td>関西みらい銀行 ／ 三菱 UFJ 銀行 ／ 三井住友銀行</td></tr>
          <tr><th>本社</th><td>〒599-8126 大阪府堺市東区大美野 171-36</td></tr>
          <tr><th>南大阪営業所</th><td>〒591-8032 大阪府堺市北区百舌鳥梅町 3-6-1</td></tr>
          <tr><th>東京営業所</th><td>〒107-0062 東京都港区南青山 2-2-15 win青山 531</td></tr>
          <tr><th>TEL</th><td><a href="tel:0722390126" style="color:var(--c-brass-2);">072-239-0126</a></td></tr>
          <tr><th>FAX</th><td>072-236-6491</td></tr>
          <tr><th>MAIL</th><td><a href="mailto:info@nichiwa-kensetu.com" style="color:var(--c-brass-2);">info@nichiwa-kensetu.com</a></td></tr>
          <tr><th>許可・登録</th><td>解体業許可証 大阪府知事 答解ー３ 1494 号<br />産業廃棄物 収集運搬</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
'''

# ============================================================
# Section 3: 沿革
# ============================================================
HISTORY_SECTION = '''<section id="history" class="history">
  <div class="container">
    <span class="eyebrow reveal">HISTORY</span>
    <h2 class="section-title reveal" style="margin-bottom:24px;">沿革。</h2>
    <p class="section-lede reveal" style="margin-bottom:48px;">外壁リフォームから始まり、塗装・アスベスト除去・解体・内装・設備まで。一歩ずつ事業領域を広げ、2021年に株式会社 日和建設として法人化しました。</p>

    <ol class="timeline-history reveal" style="max-width:880px; margin: 0 auto;">
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
# Section 4: 事業所一覧
# ============================================================
OFFICES_SECTION = '''<section id="offices" class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">OFFICES</span>
    <h2 class="section-title reveal" style="margin-bottom:48px;">事業所一覧。</h2>

    <div class="services-grid reveal-stagger" style="margin-top:48px;">
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__body" style="padding-top:40px;">
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
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__body" style="padding-top:40px;">
          <span class="card-service__num">No. 02 ／ MINAMI-OSAKA</span>
          <h3 class="card-service__title">南大阪営業所<small>SOUTH OSAKA BRANCH</small></h3>
          <p class="card-service__desc" style="line-height:2.2;">
            〒591-8032<br />
            大阪府堺市北区百舌鳥梅町 3-6-1
          </p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__body" style="padding-top:40px;">
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
# Section 5: 社員紹介
# ============================================================
EMPLOYEES_SECTION = '''<section id="people" class="section section--navy">
  <div class="container">
    <span class="eyebrow reveal">OUR PEOPLE</span>
    <h2 class="section-title reveal" style="margin-bottom:24px;">営業メンバー。</h2>
    <p class="section-lede reveal" style="margin-bottom:48px;">解体・アスベスト・塗装の現場をご依頼主・近隣の皆様につなぐ、日和建設 営業部のメンバーをご紹介します。</p>

    <div class="services-grid reveal-stagger" style="margin-top:48px;">
      <article class="card-service">
        <div class="card-service__body" style="padding-top:40px;">
          <span class="card-service__num">SALES</span>
          <h3 class="card-service__title">前田 凌<small>RYO MAEDA ／ 営業部</small></h3>
          <p class="card-service__desc">弊社に入社し、まだまだ勉強中の身ではありますが、【仕事】とは何か、常に先のことを考え予測し、人との繋がりの難しさを実感いたしました。その経験を生かし、お客様・先方様に少しでもお力になりたいと考えております。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__body" style="padding-top:40px;">
          <span class="card-service__num">SALES</span>
          <h3 class="card-service__title">伊藤 康文<small>YASUFUMI ITO ／ 営業部</small></h3>
          <p class="card-service__desc">お客様への価値のご提供と、日和建設に解体工事・アスベスト除去工事などの工事をご依頼いただいて「よかった」と言っていただけるように、日々営業活動に全力投球しています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__body" style="padding-top:40px;">
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

# ============================================================
# Section 6: 許可・資格
# ============================================================
LICENSE_SECTION = '''<section id="license" class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">LICENSE</span>
    <h2 class="section-title reveal" style="margin-bottom:48px;">許可・資格。</h2>

    <div style="max-width:760px; margin: 0 auto; text-align:center;">
      <p style="font-family:var(--ff-serif-en); font-style:italic; font-size:18px; color:var(--c-brass-2); margin-bottom:16px;">License No.</p>
      <p style="font-family:var(--ff-serif-jp); font-size:clamp(22px, 2.6vw, 32px); font-weight:600; line-height:1.7; color:var(--c-text); margin-bottom:32px;">解体業許可証<br />大阪府知事 答解ー３ 第 1494 号</p>
      <p style="font-size:14px; line-height:2; color:var(--c-text-mute);">建設リサイクル法および建設業法に基づく解体工事業の許可、ならびに産業廃棄物 収集運搬の登録を保有しています。</p>
    </div>
  </div>
</section>
'''

# ============================================================
# In-page anchor nav (sticky on PC, simple list on mobile)
# ============================================================
ANCHOR_NAV = '''<nav class="company-anchors" aria-label="ページ内ナビゲーション">
  <div class="container">
    <ul>
      <li><a href="#message">代表挨拶</a></li>
      <li><a href="#profile">会社概要</a></li>
      <li><a href="#history">沿革</a></li>
      <li><a href="#offices">事業所</a></li>
      <li><a href="#people">社員紹介</a></li>
      <li><a href="#license">許可・資格</a></li>
    </ul>
  </div>
</nav>
'''


def main():
    bc = breadcrumb_inline([("ホーム", "index.html"), ("企業情報", "")])
    html = head(
        "企業情報｜株式会社 日和建設",
        "株式会社 日和建設の企業情報。代表挨拶・会社概要・沿革・事業所一覧・社員紹介・許可資格を一覧でご紹介します。",
        "https://nichiwa-kensetu.com/company/",
        "/assets/img/message/message-hero.webp",
    )
    html += HEADER + "\n"
    html += page_hero(
        "企業情報", "COMPANY",
        "企業情報。",
        "Company",
        "代表挨拶から許可・資格まで、株式会社 日和建設に関する情報をすべてこのページにまとめています。",
        "assets/img/message/message-hero.webp",
        bc,
    )
    html += ANCHOR_NAV
    html += MESSAGE_SECTION
    html += PROFILE_SECTION
    html += HISTORY_SECTION
    html += OFFICES_SECTION
    html += EMPLOYEES_SECTION
    html += LICENSE_SECTION
    html += FOOTER
    html += "\n</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ {OUT.relative_to(ROOT)} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
