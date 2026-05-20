#!/usr/bin/env python3
"""
/strengths/ と /sustainability/ を新規生成。

構成は同業ベンチマークに準拠:
- /strengths/  → ナベカヰ「5つのポイント」型を縮約。4軸で日和の強みを語る
- /sustainability/ → 石井興業「環境方針」型を縮約。理念 + 4原則

すべて元HP nichiwa-kensetu.com の本文 + CEO挨拶から取材した実テキスト。
KPI 数字や受賞歴の捏造はしない。
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


# ============================================================
# /strengths/index.html
# ============================================================
STRENGTHS_BODY = '''<section class="section">
  <div class="container">
    <span class="eyebrow reveal">FOUR PILLARS</span>
    <h2 class="section-title reveal">私たちの、四つの強み。</h2>
    <p class="section-lede reveal" style="margin-top:24px;">日和建設は、解体・アスベスト除去・塗装の三事業を通じて、街の節目に立ち会ってきました。私たちが現場で大切にしている、四つの考え方をご紹介します。</p>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <div style="max-width:880px; margin: 0 auto;">
      <span class="eyebrow reveal">No. 01</span>
      <h3 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(24px, 3vw, 36px); font-weight:700; line-height:1.55; margin: 24px 0 32px; letter-spacing:.04em;">建物の一生を、両方向から知る。</h3>
      <div class="reveal" style="font-size:15.5px; line-height:2.2; letter-spacing:.03em;">
        <p style="margin-bottom:20px;">2017年の外壁リフォーム・塗装事業からスタートし、その後、解体工事業、アスベスト除去工事業、内装・設備・水道工事へと、事業領域を一歩ずつ広げてまいりました。</p>
        <p>「壊す」だけでなく「築く・直す」両方の現場を知っていること ── これが、解体時の判断精度につながっています。外壁の知識、塗材の性質、構造の見立て。塗装屋として培った「外壁を読む眼」が、解体・アスベスト除去のすべての工程の土台にあります。</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div style="max-width:880px; margin: 0 auto;">
      <span class="eyebrow reveal">No. 02</span>
      <h3 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(24px, 3vw, 36px); font-weight:700; line-height:1.55; margin: 24px 0 32px; letter-spacing:.04em; color: var(--c-off);">コンプライアンスと、社会的マナーの教育。</h3>
      <div class="reveal" style="font-size:15.5px; line-height:2.2; letter-spacing:.03em; color: rgba(250,250,247,.92);">
        <p style="margin-bottom:20px;">解体工事に対するイメージは、長らく不評ばかりでした。だからこそ私たちは、コンプライアンスと社会的マナーの教育に、最も力を入れて取り組んでいます。</p>
        <p>挨拶を欠かさない。近隣への配慮を忘れない。町を汚さない。──そうした<strong style="color:var(--c-brass);">当たり前を、当たり前にできる組織</strong>にすることが、代表 吉田の第一の目標です。職人全員にこの理念を共有し、現場で実践し続けることが、解体業界のイメージを変える第一歩だと考えています。</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <div style="max-width:880px; margin: 0 auto;">
      <span class="eyebrow reveal">No. 03</span>
      <h3 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(24px, 3vw, 36px); font-weight:700; line-height:1.55; margin: 24px 0 32px; letter-spacing:.04em;">アスベストへの、真摯な向き合い。</h3>
      <div class="reveal" style="font-size:15.5px; line-height:2.2; letter-spacing:.03em;">
        <p style="margin-bottom:20px;">アスベスト対策を重要な社会問題として捉え、適正な除去・処理に取り組んでいます。大気汚染防止と環境保全への配慮はもちろん、作業に従事する従業員と、その家族の健康を守る ── これがアスベスト工事業の前提です。</p>
        <p>2021年から2022年にかけて、桜塚ハイツ・垂水区一軒家・エバーケミカル工業・ヤマタネ危険物定温倉庫・橿原市平田様邸・ダクタリ動物病院・淀川ビル・鈴蘭台交番・高島屋京都店・青森県米軍基地など、<strong>計18件</strong>のアスベスト除去工事を施工してまいりました。事業詳細は <a href="services/asbestos.html" style="color:var(--c-brass-2);">アスベスト工事業</a> のページをご覧ください。</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div style="max-width:880px; margin: 0 auto;">
      <span class="eyebrow reveal">No. 04</span>
      <h3 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(24px, 3vw, 36px); font-weight:700; line-height:1.55; margin: 24px 0 32px; letter-spacing:.04em; color: var(--c-off);">三事業の、一貫対応。</h3>
      <div class="reveal" style="font-size:15.5px; line-height:2.2; letter-spacing:.03em; color: rgba(250,250,247,.92);">
        <p style="margin-bottom:20px;">解体だけ、塗装だけ、ではなく、<strong style="color:var(--c-brass);">解体・アスベスト除去・塗装の三事業を、一つの会社で受け持つ</strong>ことができます。</p>
        <p>建物の状態によっては、解体前にアスベスト含有調査が必要だったり、外壁の補修が先行したり、複数の工事が連動して必要になります。それぞれを別業者に発注する手間と引き継ぎロスを、私たちは一本化してお引き受けします。お客様の窓口は一つ。施工計画も一つ。請負金額の透明性も担保できます。</p>
      </div>
    </div>
  </div>
</section>
'''


# ============================================================
# /sustainability/index.html
# ============================================================
SUSTAINABILITY_BODY = '''<section class="section">
  <div class="container">
    <div style="max-width:760px; margin: 0 auto; text-align:center;">
      <p class="reveal" style="font-family:var(--ff-serif-en); font-style:italic; font-size:18px; color:var(--c-brass-2); margin-bottom:24px;">Our philosophy</p>
      <h2 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(28px, 3.6vw, 44px); font-weight:700; line-height:1.6; margin-bottom:40px; letter-spacing:.04em;">理念は、平和。</h2>
      <p class="reveal" style="font-size:16px; line-height:2.3; letter-spacing:.04em;">代表取締役 吉田 光輝が掲げる経営理念は、「平和」です。<br />騙し合い、いじめ、環境破壊、迷惑のない事業 ── そうした「平和な事業」を、解体業界のなかで実現していくこと。<br />それが、日和建設のサステナビリティの起点です。</p>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">FOUR PRINCIPLES</span>
    <h2 class="section-title reveal" style="margin-bottom:24px;">環境への配慮、四つの原則。</h2>
    <p class="section-lede reveal" style="margin-bottom:64px;">解体工事は、街と地球から物を引き受ける仕事です。私たちは、すべての現場でこの四つの原則を徹底しています。</p>

    <div style="max-width:880px; margin: 0 auto;">
      <article class="reveal" style="padding: 32px 0; border-top:1px solid var(--c-line);">
        <span style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass-2);">PRINCIPLE 01 ／ 大気汚染防止</span>
        <h3 style="font-family:var(--ff-serif-jp); font-size:24px; font-weight:600; margin: 16px 0 20px; line-height:1.55;">アスベストの、適正な除去・処理。</h3>
        <p style="font-size:15px; line-height:2.1;">アスベスト対策を重要な社会問題と捉え、適正な除去・処理を行います。大気汚染防止と環境保全に向けた取り組みを、すべてのアスベスト除去現場で標準にしています。</p>
      </article>

      <article class="reveal" style="padding: 32px 0; border-top:1px solid var(--c-line);">
        <span style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass-2);">PRINCIPLE 02 ／ 産業廃棄物の適正処理</span>
        <h3 style="font-family:var(--ff-serif-jp); font-size:24px; font-weight:600; margin: 16px 0 20px; line-height:1.55;">廃材を、適正な経路で。</h3>
        <p style="font-size:15px; line-height:2.1;">弊社は産業廃棄物 収集運搬の登録を保有しています。解体・アスベスト除去・塗装の各現場で発生する廃材を、適正な経路でリサイクル可能な処理場まで運搬。書類・マニフェスト管理を徹底しています。</p>
      </article>

      <article class="reveal" style="padding: 32px 0; border-top:1px solid var(--c-line);">
        <span style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass-2);">PRINCIPLE 03 ／ 近隣環境への配慮</span>
        <h3 style="font-family:var(--ff-serif-jp); font-size:24px; font-weight:600; margin: 16px 0 20px; line-height:1.55;">町を、汚さない。</h3>
        <p style="font-size:15px; line-height:2.1;">近隣への挨拶を欠かさず、町を汚さないよう環境への配慮を忘れずに作業を行う ── 職人全員に指導し続けている、現場運営の基本方針です。騒音・粉じん・搬出ルートまで、近隣の生活に寄り添う配慮を徹底します。</p>
      </article>

      <article class="reveal" style="padding: 32px 0; border-top:1px solid var(--c-line); border-bottom:1px solid var(--c-line);">
        <span style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass-2);">PRINCIPLE 04 ／ 従業員と家族の健康</span>
        <h3 style="font-family:var(--ff-serif-jp); font-size:24px; font-weight:600; margin: 16px 0 20px; line-height:1.55;">働く人の、安全のために。</h3>
        <p style="font-size:15px; line-height:2.1;">作業に従事する従業員と、その家族の健康を守るため、安全な作業環境作りに取り組んでいます。安全衛生・法令順守を徹底し、職人が安心して長く働ける現場をつくることが、私たちの社会的責任です。</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div style="max-width:760px; margin: 0 auto; text-align:center;">
      <span class="eyebrow reveal" style="justify-content:center; display:inline-flex;">TOWARD A SUSTAINABLE SOCIETY</span>
      <h2 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(24px, 3vw, 36px); font-weight:700; line-height:1.65; margin: 32px 0 32px; letter-spacing:.04em;">解体は、終わりではなく、はじまり。</h2>
      <p class="reveal" style="font-size:15.5px; line-height:2.3; letter-spacing:.03em; color: rgba(250,250,247,.9);">解体工事は終わりの工程ではなく、街が次の姿になるための前段階です。私たちはその「節目」に誠実に立ち会うことで、持続可能な社会の構築に微力ながら貢献してまいります。</p>
    </div>
  </div>
</section>
'''


PAGES = {
    "strengths/index.html": {
        "title": "強み・技術力｜株式会社 日和建設",
        "description": "日和建設の四つの強み。建物の一生を両方向から知る／コンプライアンスと社会的マナーの教育／アスベストへの真摯な向き合い／三事業の一貫対応。",
        "canonical": "https://nichiwa-kensetu.com/strengths/",
        "category": "強み・技術力",
        "category_en": "STRENGTHS",
        "h1": "私たちの、四つの強み。",
        "h1_en": "Our Strengths",
        "lede": "解体・アスベスト除去・塗装の三事業を通じて街の節目に立ち会ってきた、日和建設の考え方。",
        "bg": "assets/img/services/demolition.webp",
        "breadcrumb": [("ホーム", "index.html"), ("強み・技術力", "")],
        "body": STRENGTHS_BODY,
    },
    "sustainability/index.html": {
        "title": "サステナビリティ｜株式会社 日和建設",
        "description": "日和建設の環境方針。理念は「平和」── 大気汚染防止・産業廃棄物の適正処理・近隣環境への配慮・従業員と家族の健康の四原則。",
        "canonical": "https://nichiwa-kensetu.com/sustainability/",
        "category": "サステナビリティ",
        "category_en": "SUSTAINABILITY",
        "h1": "サステナビリティ。",
        "h1_en": "Sustainability",
        "lede": "解体工事は、街と地球から物を引き受ける仕事です。日和建設は、環境への配慮を経営理念の中心に据え、平和な事業をめざしています。",
        "bg": "assets/img/services/asbestos.webp",
        "breadcrumb": [("ホーム", "index.html"), ("サステナビリティ", "")],
        "body": SUSTAINABILITY_BODY,
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
