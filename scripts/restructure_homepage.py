#!/usr/bin/env python3
"""
index.html を構造的に再構築する。

問題点（ユーザー指摘）:
1. ABOUT カードグリッドとSERVICES カードグリッドが視覚的に重複
2. ABOUT カードは /company/#anchor に飛ぶだけでナビと完全重複
3. fabricated コピーが残っている (「建物の一生に寄り添う」「最後の敬意」等)
4. セクション数が少なく薄い

新構成:
  HEADER
  HERO (video)
  PHILOSOPHY block — 理念は、平和。(centered text + accent)
  SERVICES (3 cards, fixed titles)
  STRENGTHS teaser (text-left, image-right) — /strengths/ への誘導
  SUSTAINABILITY teaser (image-left, text-right) — /sustainability/ への誘導
  FOOTER

各セクションが異なる visual identity を持つ。

実行: python3 scripts/restructure_homepage.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"

text = INDEX.read_text(encoding="utf-8")
before_len = len(text)


# ============================================================
# (1) PHILOSOPHY (旧ABOUTカードグリッド) を、新しい理念ブロックに置換
# ============================================================
PHILOSOPHY_BLOCK = '''<!-- ============================================================
  PHILOSOPHY - 理念
============================================================ -->
<section class="section section--paper" aria-label="理念">
  <div class="container">
    <div style="max-width:760px; margin: 0 auto; text-align:center; padding: clamp(40px, 6vw, 80px) 0;">
      <p class="reveal" style="font-family:var(--ff-serif-en); font-style:italic; font-size:18px; color:var(--c-brass-2); margin-bottom:24px;">Our philosophy</p>
      <h2 class="reveal" style="font-family:var(--ff-serif-jp); font-size:clamp(36px, 5vw, 64px); font-weight:700; line-height:1.5; margin-bottom:40px; letter-spacing:.06em;">理念は、平和。</h2>
      <p class="reveal" style="font-size:16px; line-height:2.3; letter-spacing:.04em; color: var(--c-text);">騙し合い、いじめ、環境破壊、迷惑のない事業へ。<br />解体工事のイメージを、クリーンに変えていきたい。<br />日和建設は、その理念のもとで、街の節目に立ち会ってきました。</p>
      <p style="margin-top:40px;"><a class="btn-link" href="company/#message" style="color: var(--c-brass-2); border-bottom-color: var(--c-brass-2);">代表挨拶を読む</a></p>
    </div>
  </div>
</section>'''

text = re.sub(
    r'<!-- =+\s*\n\s*PHILOSOPHY.*?(?=<!-- =+\s*\n\s*SERVICES)',
    PHILOSOPHY_BLOCK + '\n\n',
    text,
    flags=re.DOTALL,
)


# ============================================================
# (2) SERVICES H2 + lede + card H3 titles を整える
# ============================================================
text = text.replace(
    '<h2 class="section-title reveal">三つの事業で、<br class="sm-only" />建物の一生に寄り添う。</h2>',
    '<h2 class="section-title reveal">三つの事業領域。</h2>',
)
text = text.replace(
    '<p class="section-lede reveal">塗装で始まり、解体・アスベスト除去まで。外壁を読む眼と、近隣を歩く足が、私たちの土台です。</p>',
    '<p class="section-lede reveal">建築リフォームから始まり、解体工事業・アスベスト除去工事業・塗装工事業の三つに広がりました。それぞれの現場で、近隣への配慮と環境保全を最優先に取り組んでいます。</p>',
)
text = text.replace(
    '<h3 class="card-service__title">建物に、最後の敬意を。<small>DEMOLITION</small></h3>',
    '<h3 class="card-service__title">解体事業<small>DISMANTLING</small></h3>',
)
text = text.replace(
    '<h3 class="card-service__title">見えないものほど、丁寧に。<small>ASBESTOS</small></h3>',
    '<h3 class="card-service__title">アスベスト工事業<small>ASBESTOS</small></h3>',
)
text = text.replace(
    '<h3 class="card-service__title">外壁の声を、最初に聴く。<small>COATING</small></h3>',
    '<h3 class="card-service__title">塗装工事業<small>COATING</small></h3>',
)
text = text.replace('解体工事の詳細へ', '解体事業を見る')
text = text.replace('アスベスト除去の詳細へ', 'アスベスト工事業を見る')
text = text.replace('塗装・外壁工事の詳細へ', '塗装工事業を見る')


# ============================================================
# (3) FOOTER の直前に「強み」と「サステナビリティ」の split teaser を挿入
# ============================================================
TEASER_BLOCKS = '''<!-- ============================================================
  STRENGTHS teaser
============================================================ -->
<section class="section section--navy" aria-label="強み・技術力">
  <div class="container">
    <div class="teaser-split reveal">
      <div class="teaser-split__text">
        <span class="eyebrow" style="margin-bottom:24px;">OUR STRENGTHS</span>
        <h2 style="font-family:var(--ff-serif-jp); font-size:clamp(28px, 3.6vw, 44px); font-weight:700; line-height:1.55; letter-spacing:.04em; margin-bottom:32px; color: var(--c-off);">私たちの、<br />四つの強み。</h2>
        <p style="font-size:15.5px; line-height:2.2; letter-spacing:.03em; color: rgba(250,250,247,.86); margin-bottom:32px;">2017年の外壁リフォームから始まり、解体・アスベスト除去・塗装の三事業へと領域を広げてきた日和建設。「壊す」と「築く」両方の現場を知ることが、私たちの判断精度を支えています。</p>
        <a class="btn-link" href="strengths/">強み・技術力を詳しく見る</a>
      </div>
      <div class="teaser-split__media">
        <img src="assets/img/strengths/strengths-hero.webp" alt="整然と並ぶ重機と分別された建材" width="800" height="600" loading="lazy" />
      </div>
    </div>
  </div>
</section>

<!-- ============================================================
  SUSTAINABILITY teaser
============================================================ -->
<section class="section section--paper" aria-label="サステナビリティ">
  <div class="container">
    <div class="teaser-split teaser-split--reverse reveal">
      <div class="teaser-split__media">
        <img src="assets/img/sustainability/sustainability-hero.webp" alt="解体跡地の整地と分別された廃材" width="800" height="600" loading="lazy" />
      </div>
      <div class="teaser-split__text">
        <span class="eyebrow" style="margin-bottom:24px;">SUSTAINABILITY</span>
        <h2 style="font-family:var(--ff-serif-jp); font-size:clamp(28px, 3.6vw, 44px); font-weight:700; line-height:1.55; letter-spacing:.04em; margin-bottom:32px; color: var(--c-text);">解体は、<br />終わりではなく、はじまり。</h2>
        <p style="font-size:15.5px; line-height:2.2; letter-spacing:.03em; color: var(--c-text); margin-bottom:32px;">解体工事は、街と地球から物を引き受ける仕事です。大気汚染防止・産業廃棄物の適正処理・近隣環境への配慮・従業員と家族の健康 ── 四つの原則を、すべての現場で徹底しています。</p>
        <a class="btn-link" href="sustainability/" style="color: var(--c-brass-2); border-bottom-color: var(--c-brass-2);">サステナビリティを詳しく見る</a>
      </div>
    </div>
  </div>
</section>

'''

text = re.sub(
    r'(?=<!-- =+\s*\n\s*FOOTER)',
    TEASER_BLOCKS,
    text,
    count=1,
)


INDEX.write_text(text, encoding="utf-8")
print(f"[OK] index.html {before_len:,} → {len(text):,} bytes ({len(text) - before_len:+,})")
