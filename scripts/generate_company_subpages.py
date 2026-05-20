#!/usr/bin/env python3
"""
/company/ 配下のサブページを既存 index.html のセクションから抽出して生成。

生成対象:
- docs/company/philosophy.html  経営理念（PHILOSOPHY セクションを完全移植）
- docs/company/message.html     代表メッセージ（CEO MESSAGE セクションを完全移植）
- docs/company/profile.html     会社概要（COMPANY セクションのテーブルを完全移植）
- docs/company/history.html     沿革・歴史（HISTORY セクションを完全移植）
- docs/company/license.html     許可・資格（短いブロック新規）

実行: python3 scripts/generate_company_subpages.py
"""
from pathlib import Path
import sys

# Import HEADER, FOOTER, head, page_hero, breadcrumb_inline from existing generator
sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline, CTA_FINAL

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# ----- philosophy.html -----
PHILOSOPHY_CONTENT = '''<section class="section section--paper">
  <div class="container">
    <div class="philosophy__inner">
      <div>
        <span class="philosophy__caption">PHILOSOPHY
          <span class="philosophy__caption-jp">経営理念</span>
        </span>
      </div>
      <div>
        <h2 class="philosophy__title reveal">
          <small>Beyond Destruction</small>
          破壊と再生の、あいだに。
        </h2>
        <div class="philosophy__body reveal">
          <p>私たちは、建物を壊すだけの会社ではありません。</p>
          <p>解体は、街が次の姿になるための前工程。だからこそ、騒音・粉じん・近隣との関係性まで、ひとつずつ丁寧に整える仕事に徹してきました。創業以来、堺の街で 1,000 を超える現場に立ち会い、その都度学び、磨いてきた作法があります。</p>
          <p>建物には、住んだ人の時間が宿ります。それを、雑に終わらせない。「日和」という社名は、晴れた日のことです。お客様にとって、どんな解体現場の翌日も、晴れであるように──それが、私たちの仕事のはじまりです。</p>
        </div>
      </div>
    </div>
    <div class="values-row reveal-stagger">
      <div class="value-item">
        <div class="value-item__label">No. 01 ／ Respect</div>
        <h3 class="value-item__title">建物への、敬意。</h3>
        <p class="value-item__body">どんな建物にも、住んだ人の時間が宿る。最後まで雑に扱わない。手で触れる工程を残し、敬意をもって解いていく。</p>
      </div>
      <div class="value-item">
        <div class="value-item__label">No. 02 ／ Care</div>
        <h3 class="value-item__title">近隣への、配慮。</h3>
        <p class="value-item__body">解体は現場の中の仕事ではなく、街の仕事。契約の前から近隣を歩き、終わるまで挨拶を絶やさない。クレームは「起こる前」に潰す。</p>
      </div>
      <div class="value-item">
        <div class="value-item__label">No. 03 ／ Integrity</div>
        <h3 class="value-item__title">仕事への、誠実。</h3>
        <p class="value-item__body">産廃マニフェストの控えはお客様にもお渡しする。記録に残し、第三者にも説明できる仕事だけを、続けていきます。</p>
      </div>
    </div>
  </div>
</section>
'''

# ----- message.html -----
MESSAGE_CONTENT = '''<section class="ceo-message section--navy">
  <div class="container">
    <div class="ceo-message__inner">
      <div class="ceo-message__portrait reveal">
        <img src="assets/img/reasons/supervisor.webp" alt="代表取締役 吉田 光輝" width="640" height="800" loading="lazy" />
      </div>
      <div>
        <span class="ceo-message__caption reveal">MESSAGE FROM CEO</span>
        <h2 class="ceo-message__title reveal">日和という名のとおり、<br />晴れた日のような仕事を。</h2>
        <div class="ceo-message__body reveal">
          <p>創業のきっかけは、ある現場での違和感でした。「壊す」という仕事が、もっと丁寧に、もっと誠実に、もっと胸を張って語れる仕事であってほしい──塗装職人として独立してから 20 年、その思いがずっと胸の中にありました。</p>
          <p>2021 年 7 月、堺の小さな事務所から日和建設は始まりました。最初に決めたのは、二つだけ。<strong>「近隣の方に、必ず頭を下げる」</strong>こと。そして<strong>「マニフェストの控えを、必ずお客様にお渡しする」</strong>こと。地味で当たり前のような約束ですが、これを 4 年間守り続けたことが、1,000 を超える現場の信頼につながったと考えています。</p>
          <p>解体は、街が次の姿になるための、はじまりの工程です。私たちはこれからも、その「はじまり」に、晴れた日のような爽やかさをもって立ち会いたい。</p>
          <p>気になることがあれば、なんでもお声がけください。お待ちしています。</p>
        </div>
        <div class="ceo-message__sign reveal">
          <span class="ceo-message__sign-label">代表取締役</span>
          <span class="ceo-message__sign-name">吉田 光輝</span>
        </div>
      </div>
    </div>
  </div>
</section>
'''

# ----- profile.html -----
PROFILE_CONTENT = '''<section class="section section--navy">
  <div class="container">
    <span class="eyebrow reveal">COMPANY PROFILE</span>
    <h2 class="section-title reveal">堺で生まれた、誠実な仕事のこと。</h2>

    <div class="company-layout">
      <div class="reveal">
        <table class="company-table">
          <tbody>
            <tr><th>商号 ／ Name</th><td>株式会社 日和建設（NICHIWA KENSETSU CO., LTD.）</td></tr>
            <tr><th>設立 ／ Founded</th><td>2021年 7 月 2 日</td></tr>
            <tr><th>代表 ／ CEO</th><td>吉田 光輝</td></tr>
            <tr><th>資本金 ／ Capital</th><td>500 万円</td></tr>
            <tr><th>従業員 ／ Staff</th><td>30 名</td></tr>
            <tr><th>本社 ／ HQ</th><td>〒599-8126 大阪府堺市東区大美野 171-36</td></tr>
            <tr><th>営業所 ／ Branches</th><td>南大阪営業所 ／ 東京営業所（全国対応）</td></tr>
            <tr><th>事業 ／ Services</th><td>解体工事 ／ アスベスト除去工事 ／ 塗装・外壁工事</td></tr>
            <tr><th>許可 ／ License</th><td>大阪府知事 解体業許可 第 1494 号</td></tr>
            <tr><th>連絡先 ／ Contact</th><td><a href="tel:0722390126" style="color:var(--c-brass);">072-239-0126</a> ／ info@nichiwa-kensetu.com</td></tr>
          </tbody>
        </table>
      </div>

      <aside class="company-aside reveal">
        <img src="assets/img/company/permit.webp" alt="解体業許可証イメージ" width="720" height="900" loading="lazy" />
        <blockquote class="company-message">
          「日和」という社名は、晴れた日のことです。<br />
          お客様にとって、どんな解体現場の翌日も、晴れであるように。
          <footer>― 代表取締役　吉田 光輝</footer>
        </blockquote>
      </aside>
    </div>
  </div>
</section>
'''

# ----- history.html -----
HISTORY_CONTENT = '''<section class="history">
  <div class="container">
    <span class="eyebrow reveal">HISTORY</span>
    <h2 class="section-title reveal">堺の小さな会社の、これまで。</h2>
    <p class="section-lede reveal">2021 年 7 月、堺の事務所で 5 名から始まりました。創業から 4 年で立ち会わせていただいた現場と、お客様への感謝の積み重ねです。</p>

    <ol class="timeline-history reveal">
      <li>
        <span class="timeline-history__year">2021.07</span>
        <div>
          <h3 class="timeline-history__title">株式会社 日和建設 創業</h3>
          <p class="timeline-history__body">大阪府堺市東区大美野にて創業。代表取締役 吉田 光輝。資本金 500 万円、従業員 5 名でのスタート。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2022.04</span>
        <div>
          <h3 class="timeline-history__title">解体実績 累計 100 件 達成</h3>
          <p class="timeline-history__body">堺市・大阪市内を中心に、木造戸建ての解体を中心に実績を積み上げ。創業 9 ヶ月で 100 件のマイルストーンを達成。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2023.06</span>
        <div>
          <h3 class="timeline-history__title">南大阪営業所 開設</h3>
          <p class="timeline-history__body">大阪府南部・和歌山方面への対応強化のため、南大阪営業所を新設。RC造解体とアスベスト除去の専任チームを編成。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2024.03</span>
        <div>
          <h3 class="timeline-history__title">アスベスト除去 累計 500 件 達成</h3>
          <p class="timeline-history__body">レベル 1 〜 3 の石綿含有建材除去工事の累計実績が 500 件を突破。建築物石綿含有建材調査者の資格保有者を 3 名体制に拡充。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2025.09</span>
        <div>
          <h3 class="timeline-history__title">東京営業所 開設・全国対応開始</h3>
          <p class="timeline-history__body">関東圏の案件増加を受け、東京営業所を新設。これにより全国対応体制が整い、従業員数は 30 名に。</p>
        </div>
      </li>
      <li>
        <span class="timeline-history__year">2026.04</span>
        <div>
          <h3 class="timeline-history__title">解体実績 累計 1,000 件 突破</h3>
          <p class="timeline-history__body">創業から 4 年 9 ヶ月で、解体工事の累計実績が 1,000 件を達成。あわせてコーポレートサイトを全面リニューアル。</p>
        </div>
      </li>
    </ol>
  </div>
</section>
'''

# ----- license.html -----
LICENSE_CONTENT = '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">LICENSE & CERTIFICATIONS</span>
    <h2 class="section-title reveal">許可・資格・所属団体</h2>
    <p class="section-lede reveal">解体工事業を含む特定建設業を行うために必要な、行政許可・有資格者・所属団体をすべて公開しています。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service" style="background: var(--c-paper); color: var(--c-ink);">
        <div class="card-service__media">
          <img src="assets/img/company/permit.webp" alt="解体業許可証" loading="lazy" />
        </div>
        <div class="card-service__body" style="color: var(--c-ink);">
          <span class="card-service__num">LICENSE</span>
          <h3 class="card-service__title" style="color: var(--c-ink);">解体業 許可<small>DEMOLITION</small></h3>
          <p class="card-service__desc" style="color: rgba(15, 27, 45, .72);">大阪府知事 解体業許可 第 1494 号。建設リサイクル法および建設業法に基づく解体工事業の許可を保有しています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-paper); color: var(--c-ink);">
        <div class="card-service__media">
          <img src="assets/img/services/asbestos.webp" alt="アスベスト関連資格" loading="lazy" />
        </div>
        <div class="card-service__body" style="color: var(--c-ink);">
          <span class="card-service__num">CERTIFICATIONS</span>
          <h3 class="card-service__title" style="color: var(--c-ink);">建築物石綿含有建材調査者<small>ASBESTOS SURVEYOR</small></h3>
          <p class="card-service__desc" style="color: rgba(15, 27, 45, .72);">石綿含有建材の事前調査を法令通りに実施するため、当社では国家資格「建築物石綿含有建材調査者」の保有者を 3 名体制で配置しています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-paper); color: var(--c-ink);">
        <div class="card-service__media">
          <img src="assets/img/services/coating.webp" alt="塗装関連資格" loading="lazy" />
        </div>
        <div class="card-service__body" style="color: var(--c-ink);">
          <span class="card-service__num">SAFETY</span>
          <h3 class="card-service__title" style="color: var(--c-ink);">安全管理体制<small>SAFETY MANAGEMENT</small></h3>
          <p class="card-service__desc" style="color: rgba(15, 27, 45, .72);">職長・安全衛生責任者教育修了者、車両系建設機械運転技能講習修了者、玉掛け技能講習修了者など、各現場で必要な有資格者を配置しています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
    </div>
  </div>
</section>
'''

# ============================================================

PAGES = {
    "company/philosophy.html": {
        "title": "経営理念｜株式会社 日和建設",
        "description": "日和建設の経営理念「破壊と再生の、あいだに。」。建物への敬意・近隣への配慮・仕事への誠実、三つの価値観をご紹介します。",
        "canonical": "https://nichiwa-kensetu.com/company/philosophy.html",
        "category": "経営理念",
        "category_en": "PHILOSOPHY",
        "h1": "破壊と再生の、あいだに。",
        "h1_en": "Beyond Destruction",
        "lede": "私たちは、建物を壊すだけの会社ではありません。解体は、街が次の姿になるための前工程。だからこそ、騒音・粉じん・近隣との関係性まで、ひとつずつ丁寧に整える仕事に徹してきました。",
        "bg": "assets/img/hero/hero-real.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("経営理念", "")],
        "content": PHILOSOPHY_CONTENT,
    },
    "company/message.html": {
        "title": "代表メッセージ｜株式会社 日和建設",
        "description": "代表取締役 吉田 光輝より、日和建設創業の背景と仕事への想いをお伝えします。「近隣の方に必ず頭を下げる」「マニフェストの控えを必ずお渡しする」。",
        "canonical": "https://nichiwa-kensetu.com/company/message.html",
        "category": "代表メッセージ",
        "category_en": "MESSAGE",
        "h1": "晴れた日のような仕事を。",
        "h1_en": "Message from CEO",
        "lede": "「壊す」という仕事が、もっと丁寧に、もっと誠実に、もっと胸を張って語れる仕事であってほしい ── 代表取締役 吉田 光輝より。",
        "bg": "assets/img/reasons/supervisor.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("代表メッセージ", "")],
        "content": MESSAGE_CONTENT,
    },
    "company/profile.html": {
        "title": "会社概要｜株式会社 日和建設",
        "description": "株式会社 日和建設の会社概要。商号、設立、代表、資本金、従業員、本社・営業所、事業、許可番号、連絡先。",
        "canonical": "https://nichiwa-kensetu.com/company/profile.html",
        "category": "会社概要",
        "category_en": "PROFILE",
        "h1": "会社概要",
        "h1_en": "Company Profile",
        "lede": "株式会社 日和建設の基本情報をご紹介します。商号、設立、代表、所在地、事業、許認可など。",
        "bg": "assets/img/services/coating.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("会社概要", "")],
        "content": PROFILE_CONTENT,
    },
    "company/history.html": {
        "title": "沿革・歴史｜株式会社 日和建設",
        "description": "2021年7月、堺の事務所で5名から始まりました。創業から4年で立ち会わせていただいた現場の積み重ねです。",
        "canonical": "https://nichiwa-kensetu.com/company/history.html",
        "category": "沿革・歴史",
        "category_en": "HISTORY",
        "h1": "堺の小さな会社の、これまで。",
        "h1_en": "Our History",
        "lede": "2021 年 7 月、堺の事務所で 5 名から始まりました。創業から 4 年で立ち会わせていただいた現場と、お客様への感謝の積み重ねです。",
        "bg": "assets/img/services/demolition.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("沿革・歴史", "")],
        "content": HISTORY_CONTENT,
    },
    "company/license.html": {
        "title": "許可・資格｜株式会社 日和建設",
        "description": "大阪府知事 解体業許可 第1494号。建築物石綿含有建材調査者3名体制。職長教育、車両系運転技能講習修了者を各現場配置。",
        "canonical": "https://nichiwa-kensetu.com/company/license.html",
        "category": "許可・資格",
        "category_en": "LICENSE",
        "h1": "許可・資格・所属団体",
        "h1_en": "License & Certifications",
        "lede": "解体工事業を行うために必要な行政許可、有資格者、所属団体をすべて公開しています。",
        "bg": "assets/img/company/permit.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("許可・資格", "")],
        "content": LICENSE_CONTENT,
    },
}


def main():
    for rel, cfg in PAGES.items():
        path = DOCS / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        bc = breadcrumb_inline(cfg["breadcrumb"])
        html = ""
        html += head(cfg["title"], cfg["description"], cfg["canonical"], "/" + cfg["bg"])
        html += HEADER + "\n"
        html += page_hero(cfg["category"], cfg["category_en"], cfg["h1"], cfg["h1_en"], cfg["lede"], cfg["bg"], bc)
        html += cfg["content"]
        html += CTA_FINAL
        html += FOOTER
        html += "\n</body>\n</html>\n"
        path.write_text(html, encoding="utf-8")
        print(f"✓ {rel} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
