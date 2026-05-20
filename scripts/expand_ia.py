#!/usr/bin/env python3
"""
recruit.co.jp相当のIA深度へ拡張。新規5ページ生成。

生成対象:
- docs/company/leadership.html   役員一覧
- docs/company/offices.html      事業所一覧
- docs/company/foundation.html   企業活動の重要な基盤
- docs/culture/index.html        人的資本経営
- docs/blog/index.html           ブログ（プレースホルダ＋3記事スタブ）

実行: python3 scripts/expand_ia.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline, CTA_FINAL

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


# ============================================================
# /company/leadership.html — 役員一覧
# ============================================================
LEADERSHIP_BODY = '''<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">REPRESENTATIVE</span>
    <h2 class="section-title reveal">代表取締役。</h2>

    <div class="leader-feature reveal" style="margin-top:64px; display:grid; grid-template-columns: 1fr 1.4fr; gap:64px; align-items:start;">
      <div>
        <img src="assets/img/reasons/supervisor.webp" alt="代表取締役 吉田 光輝" style="width:100%; aspect-ratio: 4/5; object-fit: cover;" loading="lazy" />
        <p style="margin-top:16px; font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass);">CEO / FOUNDER</p>
      </div>
      <div>
        <p style="font-family:var(--ff-serif-en); font-style:italic; font-size:20px; color:var(--c-brass); margin-bottom:8px;">Mitsuteru Yoshida</p>
        <h3 style="font-family:var(--ff-serif-jp); font-size:36px; font-weight:600; margin:0 0 32px 0;">吉田 光輝</h3>
        <p style="font-size:14px; color:var(--c-text-mute); letter-spacing:.04em; line-height:2; margin-bottom:24px;"><strong style="color:var(--c-text); font-weight:600;">代表取締役</strong>　／　Founder &amp; CEO</p>
        <div style="font-size:15px; line-height:2.1; color:var(--c-text);">
          <p style="margin-bottom:20px;">2001年、塗装職人として独立。20年にわたり外装現場の最前線に立ち、解体・アスベスト工事における「外壁を読む眼」の重要性を見出す。</p>
          <p style="margin-bottom:20px;">2021年7月、堺市東区にて株式会社 日和建設を創業。「壊すだけでは、終わらない」を経営理念とし、近隣合意形成を契約より先に置く施工管理を実践。</p>
          <p>創業4年で解体実績1,000件超、アスベスト除去500件超を達成。重大クレーム発生ゼロ。</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow reveal">DIRECTORS &amp; MANAGERS</span>
    <h2 class="section-title reveal">経営陣・主要メンバー。</h2>
    <p class="section-lede reveal">現場を知る経営層が、日々の現場と経営の両輪を回しています。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service">
        <div class="card-service__media" style="aspect-ratio: 1/1;">
          <div style="width:100%; height:100%; background: linear-gradient(135deg, var(--c-navy-light, #1a2942) 0%, var(--c-navy) 100%); display:flex; align-items:center; justify-content:center;">
            <span style="font-family:var(--ff-serif-en); font-size:64px; font-style:italic; color:var(--c-brass); opacity:.4;">T</span>
          </div>
        </div>
        <div class="card-service__body">
          <span class="card-service__num">DIRECTOR</span>
          <h3 class="card-service__title">取締役 / 営業統括<small>SALES DIVISION HEAD</small></h3>
          <p class="card-service__desc">15年以上の解体工事営業経験。顧客折衝・見積精度・近隣調整の戦略を統括し、全国対応体制を構築。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media" style="aspect-ratio: 1/1;">
          <div style="width:100%; height:100%; background: linear-gradient(135deg, var(--c-navy-light, #1a2942) 0%, var(--c-navy) 100%); display:flex; align-items:center; justify-content:center;">
            <span style="font-family:var(--ff-serif-en); font-size:64px; font-style:italic; color:var(--c-brass); opacity:.4;">K</span>
          </div>
        </div>
        <div class="card-service__body">
          <span class="card-service__num">DIRECTOR</span>
          <h3 class="card-service__title">取締役 / 工事統括<small>OPERATIONS HEAD</small></h3>
          <p class="card-service__desc">建築物石綿含有建材調査者。アスベスト除去工事の全現場で行政手続き・施工管理・第三者報告まで一括統括。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media" style="aspect-ratio: 1/1;">
          <div style="width:100%; height:100%; background: linear-gradient(135deg, var(--c-navy-light, #1a2942) 0%, var(--c-navy) 100%); display:flex; align-items:center; justify-content:center;">
            <span style="font-family:var(--ff-serif-en); font-size:64px; font-style:italic; color:var(--c-brass); opacity:.4;">S</span>
          </div>
        </div>
        <div class="card-service__body">
          <span class="card-service__num">MANAGER</span>
          <h3 class="card-service__title">現場監督チーフ<small>SITE SUPERVISOR LEAD</small></h3>
          <p class="card-service__desc">10名超の現場監督チームを統括。LINE日報体制で全現場を毎日可視化し、施主・近隣・職人の三方向に情報共有。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
    </div>
    <p style="margin-top:48px; font-size:13px; color:var(--c-text-mute); text-align:center;">※ 個人情報保護の観点から、姓のみ掲載しております。</p>
  </div>
</section>
'''

# ============================================================
# /company/offices.html — 事業所一覧
# ============================================================
OFFICES_BODY = '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">OUR OFFICES</span>
    <h2 class="section-title reveal">三拠点で、全国を。</h2>
    <p class="section-lede reveal">本社（堺）／南大阪営業所／東京営業所の三拠点体制。関西全域および関東圏での施工に対応します。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/hero/hero-real.webp" alt="本社外観" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">No. 01 ／ HQ</span>
          <h3 class="card-service__title">本社<small>HEADQUARTERS — SAKAI</small></h3>
          <p class="card-service__desc"><strong>〒599-8126</strong><br />大阪府堺市東区大美野 171-36<br />TEL <a href="tel:0722390126" style="color:var(--c-brass);">072-239-0126</a><br />FAX 072-236-6491</p>
          <p style="font-size:13px; color:var(--c-text-mute); margin-top:8px;">対応エリア: 大阪府全域・兵庫県・京都府・奈良県・和歌山県</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/demolition.webp" alt="南大阪営業所" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">No. 02 ／ MINAMI-OSAKA</span>
          <h3 class="card-service__title">南大阪営業所<small>SOUTH OSAKA BRANCH</small></h3>
          <p class="card-service__desc">RC造解体・アスベスト除去の専任チーム拠点。大阪府南部・和歌山方面の現場に対応。<br /><br />2023年6月開設。</p>
          <p style="font-size:13px; color:var(--c-text-mute); margin-top:8px;">対応エリア: 大阪府南部・和歌山県</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/coating.webp" alt="東京営業所" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">No. 03 ／ TOKYO</span>
          <h3 class="card-service__title">東京営業所<small>TOKYO BRANCH</small></h3>
          <p class="card-service__desc">関東圏案件の窓口拠点。首都圏のオフィスビル・商業施設の解体工事に対応。<br /><br />2025年9月開設。</p>
          <p style="font-size:13px; color:var(--c-text-mute); margin-top:8px;">対応エリア: 東京都・神奈川県・千葉県・埼玉県</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">COVERAGE</span>
    <h2 class="section-title reveal">対応エリア。</h2>

    <div style="margin-top:48px; display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:32px;">
      <div>
        <strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">KANSAI ／ 関西エリア</strong>
        <p style="margin-top:12px; line-height:2;">大阪府全域<br />兵庫県（神戸市・尼崎市等）<br />京都府（京都市・宇治市等）<br />奈良県・和歌山県</p>
      </div>
      <div>
        <strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">KANTO ／ 関東エリア</strong>
        <p style="margin-top:12px; line-height:2;">東京都（23区・多摩地区）<br />神奈川県（横浜市・川崎市）<br />千葉県・埼玉県</p>
      </div>
      <div>
        <strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">OTHER ／ その他</strong>
        <p style="margin-top:12px; line-height:2;">上記以外の地域も、案件規模によりご相談に応じます。まずはお問い合わせください。</p>
      </div>
    </div>
  </div>
</section>
'''

# ============================================================
# /company/foundation.html — 企業活動の重要な基盤
# ============================================================
FOUNDATION_BODY = '''<section class="section section--paper">
  <div class="container">
    <div style="display:grid; grid-template-columns: 1fr 2fr; gap:80px; align-items:start;">
      <div>
        <span class="eyebrow reveal">OUR FOUNDATION</span>
      </div>
      <div>
        <h2 class="section-title reveal" style="margin-bottom:32px;">仕事の土台にあるのは、<br />ルールではなく、誠実です。</h2>
        <p class="section-lede reveal" style="font-size:16px;">建設業の社会的責任は、年々重くなっています。解体工事業者として、産業廃棄物・アスベスト・労働安全衛生・近隣関係 ── これらすべてに、第三者に説明できる基準で向き合うこと。私たちは、その「当たり前」を、誠実に守り続けることだけを、土台にしてきました。</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow reveal">FOUR PILLARS</span>
    <h2 class="section-title reveal">四つの柱。</h2>

    <ol class="reasons-list reveal" style="margin-top:48px; max-width:none;">
      <li class="reason">
        <span class="reason__num">No. 01</span>
        <h3 class="reason__title">ガバナンス <small style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); margin-left:12px;">GOVERNANCE</small></h3>
        <p class="reason__body">代表取締役・取締役・現場監督チーフによる毎月の経営会議で、安全管理・契約・財務・近隣対応のすべてをレビュー。全現場の状況は社内チャットでリアルタイム共有し、属人化を排しています。</p>
      </li>
      <li class="reason">
        <span class="reason__num">No. 02</span>
        <h3 class="reason__title">コンプライアンス <small style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); margin-left:12px;">COMPLIANCE</small></h3>
        <p class="reason__body">建設リサイクル法・大気汚染防止法・労働安全衛生法・廃棄物処理法、すべて法令順守の徹底。産廃マニフェストは元請から処分まで一気通貫で管理し、控えはすべてお客様にもお渡しします。</p>
      </li>
      <li class="reason">
        <span class="reason__num">No. 03</span>
        <h3 class="reason__title">リスクマネジメント <small style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); margin-left:12px;">RISK MANAGEMENT</small></h3>
        <p class="reason__body">労災ゼロを目標とし、KY活動（危険予知）を全現場で毎朝実施。建設業労災総合保険、施工保証、近隣家屋事前調査も標準仕様。アスベスト除去現場は大気濃度測定で第三者検証可能な記録を残します。</p>
      </li>
      <li class="reason">
        <span class="reason__num">No. 04</span>
        <h3 class="reason__title">倫理 <small style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); margin-left:12px;">ETHICS</small></h3>
        <p class="reason__body">「近隣の方に、必ず頭を下げる」「マニフェストの控えを、必ずお客様にお渡しする」── 創業時に決めた二つの約束を、4年間 1,000件超の現場で守り続けています。地味な約束を続けることが、信頼の土台です。</p>
      </li>
    </ol>
  </div>
</section>
'''

# ============================================================
# /culture/index.html — 人的資本経営
# ============================================================
CULTURE_BODY = '''<section class="section section--navy">
  <div class="container">
    <span class="eyebrow reveal">OUR PEOPLE</span>
    <h2 class="section-title reveal">価値の源泉は、現場にいる、ひとり、ひとり。</h2>
    <p class="section-lede reveal">日和建設は 30 名の小さな会社です。だからこそ、ひとりの仕事が、街の景色を変えます。私たちは、その重みを大切にする会社でありたい。</p>

    <div class="kpi-grid" style="margin-top:64px;">
      <div class="kpi">
        <span class="kpi__num-wrap"><span class="kpi__num" data-target="30">0</span><span class="kpi__plus" aria-hidden="true">名</span></span>
        <p class="kpi__caption">従業員数<br /><span style="opacity:.6">STAFF</span></p>
        <span class="kpi__bar" aria-hidden="true"></span>
      </div>
      <div class="kpi">
        <span class="kpi__num-wrap"><span class="kpi__num" data-target="98">0</span><span class="kpi__plus" aria-hidden="true">%</span></span>
        <p class="kpi__caption">資格保有率<br /><span style="opacity:.6">CERTIFIED</span></p>
        <span class="kpi__bar" aria-hidden="true"></span>
      </div>
      <div class="kpi">
        <span class="kpi__num-wrap"><span class="kpi__num" data-target="3">0</span><span class="kpi__plus" aria-hidden="true">名</span></span>
        <p class="kpi__caption">石綿含有建材調査者<br /><span style="opacity:.6">ASBESTOS SURVEYOR</span></p>
        <span class="kpi__bar" aria-hidden="true"></span>
      </div>
      <div class="kpi kpi--zero">
        <span class="kpi__num-wrap"><span class="kpi__num" data-target="0">0</span></span>
        <p class="kpi__caption">重大労災発生<br /><span style="opacity:.6">ZERO</span></p>
        <span class="kpi__bar" aria-hidden="true"></span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow reveal">CULTURE</span>
    <h2 class="section-title reveal">三つの文化。</h2>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/demolition.webp" alt="現場第一" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">CULTURE 01</span>
          <h3 class="card-service__title">現場が、経営の中心。<small>FIELD-FIRST</small></h3>
          <p class="card-service__desc">経営会議も、戦略の起点も、現場の声から。経営層が現場に立つ「フィールドファースト」の文化を、創業から守り続けています。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/services/coating.webp" alt="育てる文化" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">CULTURE 02</span>
          <h3 class="card-service__title">資格は、会社が育てる。<small>EDUCATION</small></h3>
          <p class="card-service__desc">建築物石綿含有建材調査者、車両系建設機械、玉掛け、職長教育 ── 資格取得は全額会社負担。学びたい人が、止められない仕組みです。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media">
          <img src="assets/img/reasons/supervisor.webp" alt="長く働ける" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">CULTURE 03</span>
          <h3 class="card-service__title">長く、続けられる仕事に。<small>SUSTAINABILITY</small></h3>
          <p class="card-service__desc">週休制、夏期冬期休暇、社会保険完備。職人が定年まで続けられる現場を、経営として整えるのが、私たちの責任です。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">JOIN US</span>
    <h2 class="section-title reveal">仲間を、募集しています。</h2>
    <p class="section-lede reveal">現場監督候補・職人・営業 ── すべての職種で、新卒・経験者ともに採用を行っています。</p>
    <div style="margin-top:40px;">
      <a class="btn btn-gold" href="recruit.html"><span>採用情報を見る</span><span class="arrow" aria-hidden="true"></span></a>
    </div>
  </div>
</section>
'''

# ============================================================
# /blog/index.html — ブログトップ
# ============================================================
BLOG_BODY = '''<section class="section">
  <div class="container">
    <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:24px; margin-bottom:48px;">
      <span class="eyebrow reveal">CATEGORIES</span>
      <nav aria-label="ブログカテゴリ" style="display:flex; gap:24px; flex-wrap:wrap;">
        <a href="#" style="font-size:13px; letter-spacing:.04em; padding:8px 0; border-bottom:1px solid var(--c-brass); color:var(--c-text);">すべて</a>
        <a href="#" style="font-size:13px; letter-spacing:.04em; padding:8px 0; color:var(--c-text-mute);">現場レポート</a>
        <a href="#" style="font-size:13px; letter-spacing:.04em; padding:8px 0; color:var(--c-text-mute);">職人ストーリー</a>
        <a href="#" style="font-size:13px; letter-spacing:.04em; padding:8px 0; color:var(--c-text-mute);">業界トピック</a>
        <a href="#" style="font-size:13px; letter-spacing:.04em; padding:8px 0; color:var(--c-text-mute);">採用・カルチャー</a>
      </nav>
    </div>

    <article style="display:grid; grid-template-columns: 1.4fr 1fr; gap:48px; align-items:center; padding:48px 0; border-top:1px solid var(--c-line); border-bottom:1px solid var(--c-line);">
      <div>
        <div style="display:flex; gap:16px; margin-bottom:16px; font-size:11px; letter-spacing:.24em;"><span style="color:var(--c-brass);">FEATURED</span><span style="color:var(--c-text-mute);">2026.05.15</span><span style="color:var(--c-text-mute);">現場レポート</span></div>
        <h3 style="font-family:var(--ff-serif-jp); font-size:32px; font-weight:600; line-height:1.5; margin-bottom:24px;">仁徳ビル 階上解体工事完工レポート。<br />隣接敷地 50cm の難条件で、事故ゼロ。</h3>
        <p style="font-size:15px; line-height:2; color:var(--c-text-mute); margin-bottom:24px;">商業ビル密集地帯で、隣接建物との離隔が片側 50cm という難条件の階上解体工事。低騒音重機の選定、養生範囲の拡大、毎朝の KY 活動の徹底で、無事故・無クレームで完工した記録です。</p>
        <a class="btn-link" href="#">記事を読む</a>
      </div>
      <div>
        <img src="assets/img/works/work-02.webp" alt="仁徳ビル 階上解体工事" style="width:100%; aspect-ratio:4/3; object-fit:cover;" loading="lazy" />
      </div>
    </article>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow reveal">RECENT POSTS</span>
    <h2 class="section-title reveal">最近の記事。</h2>

    <div class="services-grid reveal-stagger" style="margin-top:48px;">
      <article class="card-service">
        <div class="card-service__media"><img src="assets/img/services/asbestos.webp" alt="アスベスト除去現場ルポ" loading="lazy" /></div>
        <div class="card-service__body">
          <span class="card-service__num">2026.04.28 ／ 現場レポート</span>
          <h3 class="card-service__title">アスベスト除去レベル1、密閉養生のすべて。<small>FIELD REPORT</small></h3>
          <p class="card-service__desc">石綿含有吹付建材の除去現場で、密閉養生・負圧除じん・湿潤化 ── 三段階の手順を写真とともに公開します。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="#">記事を読む</a>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media"><img src="assets/img/reasons/supervisor.webp" alt="職人ストーリー" loading="lazy" /></div>
        <div class="card-service__body">
          <span class="card-service__num">2026.04.10 ／ 職人ストーリー</span>
          <h3 class="card-service__title">塗装から解体へ。35年現場の話。<small>CRAFTSMAN STORY</small></h3>
          <p class="card-service__desc">創業時から日和建設を支える、現場監督チーフ S が語る、塗装から解体へ移った理由と、現場で大切にしていること。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="#">記事を読む</a>
        </div>
      </article>
      <article class="card-service">
        <div class="card-service__media"><img src="assets/img/services/coating.webp" alt="業界トピック" loading="lazy" /></div>
        <div class="card-service__body">
          <span class="card-service__num">2026.03.20 ／ 業界トピック</span>
          <h3 class="card-service__title">2026年改正石綿則を、現場目線で読む。<small>INDUSTRY UPDATE</small></h3>
          <p class="card-service__desc">2026年4月施行の改正石綿則。事前調査・記録保存・大気濃度測定 ── 現場で何が変わるか、解体業者目線で解説します。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="#">記事を読む</a>
        </div>
      </article>
    </div>

    <p style="margin-top:64px; text-align:center; color:var(--c-text-mute); font-size:14px;">※ 記事は順次公開予定です。お知らせ一覧でも更新情報をお届けします。</p>
  </div>
</section>
'''


PAGES = {
    "company/leadership.html": {
        "title": "役員一覧｜株式会社 日和建設",
        "description": "代表取締役 吉田 光輝、取締役 営業統括、取締役 工事統括、現場監督チーフ。日和建設の経営陣・主要メンバーをご紹介します。",
        "canonical": "https://nichiwa-kensetu.com/company/leadership.html",
        "category": "役員一覧",
        "category_en": "LEADERSHIP",
        "h1": "現場を、知る経営。",
        "h1_en": "Leadership",
        "lede": "創業者・代表取締役 吉田 光輝をはじめ、日和建設の経営層は全員、現場で20年以上の経験を持つ実務家です。経営会議の起点は、いつも現場の声から。",
        "bg": "assets/img/reasons/supervisor.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("役員一覧", "")],
        "body": LEADERSHIP_BODY,
    },
    "company/offices.html": {
        "title": "事業所一覧｜株式会社 日和建設",
        "description": "本社（堺市東区）／南大阪営業所／東京営業所の三拠点体制。関西全域および関東圏の解体・アスベスト・塗装工事に対応します。",
        "canonical": "https://nichiwa-kensetu.com/company/offices.html",
        "category": "事業所一覧",
        "category_en": "OFFICES",
        "h1": "三拠点で、全国を。",
        "h1_en": "Offices",
        "lede": "本社（堺）／南大阪営業所／東京営業所の三拠点体制で、関西全域および関東圏での施工に対応します。地域に根ざした営業所と、本社の専門家チームが連携しています。",
        "bg": "assets/img/hero/hero-real.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("事業所一覧", "")],
        "body": OFFICES_BODY,
    },
    "company/foundation.html": {
        "title": "企業活動の基盤｜株式会社 日和建設",
        "description": "ガバナンス・コンプライアンス・リスクマネジメント・倫理 ── 日和建設の企業活動を支える4つの柱。",
        "canonical": "https://nichiwa-kensetu.com/company/foundation.html",
        "category": "企業活動の基盤",
        "category_en": "FOUNDATION",
        "h1": "誠実が、土台のすべて。",
        "h1_en": "Our Foundation",
        "lede": "建設業の社会的責任は年々重くなっています。私たちは「ガバナンス・コンプライアンス・リスクマネジメント・倫理」の四つの柱を、特別なことではなく、当たり前のこととして守り続けてきました。",
        "bg": "assets/img/company/permit.webp",
        "breadcrumb": [("ホーム", "index.html"), ("企業情報", "company/"), ("企業活動の基盤", "")],
        "body": FOUNDATION_BODY,
    },
    "culture/index.html": {
        "title": "人的資本経営｜株式会社 日和建設",
        "description": "従業員30名、資格保有率98%、重大労災ゼロ。現場第一・育成・長く続けられる仕事の3つの文化で、人を大切にする会社を目指します。",
        "canonical": "https://nichiwa-kensetu.com/culture/",
        "category": "人的資本経営",
        "category_en": "OUR PEOPLE",
        "h1": "価値の源泉は、人。",
        "h1_en": "Human Capital",
        "lede": "日和建設は30名の小さな会社です。だからこそ、ひとりの仕事が街の景色を変える。私たちは、その重みを大切にする会社でありたい。",
        "bg": "assets/img/reasons/supervisor.webp",
        "breadcrumb": [("ホーム", "index.html"), ("人的資本経営", "")],
        "body": CULTURE_BODY,
    },
    "blog/index.html": {
        "title": "ブログ｜株式会社 日和建設",
        "description": "現場レポート、職人ストーリー、業界トピック、採用・カルチャー。日和建設の日々を、現場の目線でお届けします。",
        "canonical": "https://nichiwa-kensetu.com/blog/",
        "category": "ブログ",
        "category_en": "BLOG",
        "h1": "現場から、街へ。",
        "h1_en": "Field Notes",
        "lede": "現場レポート、職人ストーリー、業界トピック、採用・カルチャー ── 日和建設の日々を、現場の目線でお届けします。",
        "bg": "assets/img/services/demolition.webp",
        "breadcrumb": [("ホーム", "index.html"), ("ブログ", "")],
        "body": BLOG_BODY,
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
