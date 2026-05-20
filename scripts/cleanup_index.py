#!/usr/bin/env python3
"""
index.html から架空コンテンツを削除＆実データに置換。

削除対象（架空）:
- KPI 1000/500/300/0 セクション
- WHY teaser「4つの理由」+ /strengths/ リンク
- SUSTAINABILITY 92%/98%/0 セクション
- ABOUT teaser の "philosophy.html" リンク（削除済ページ）
- ABOUT lede 内の "1,000 を超える現場" 言及

実データに置換:
- ABOUT lede → 実CEO message から抜粋
- ABOUT teaser philosophy card → "代表挨拶" (実在) へ
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"

text = INDEX.read_text(encoding="utf-8")
original_len = len(text)

# 1) KPI セクション全削除
text = re.sub(
    r'<!-- =+\s*\n\s*KPI.*?(?=<!-- =+\s*\n\s*SERVICES)',
    '',
    text,
    flags=re.DOTALL,
)

# 2) WHY セクション全削除
text = re.sub(
    r'<!-- =+\s*\n\s*WHY.*?(?=<!-- =+\s*\n\s*WORKS)',
    '',
    text,
    flags=re.DOTALL,
)

# 3) SUSTAINABILITY セクション全削除
text = re.sub(
    r'<!-- =+\s*\n\s*SUSTAINABILITY.*?(?=<!-- =+\s*\n\s*NEWS)',
    '',
    text,
    flags=re.DOTALL,
)

# 3b) NEWS セクション全削除（実ニュースなし）
text = re.sub(
    r'<!-- =+\s*\n\s*NEWS.*?(?=<!-- =+\s*\n\s*(?:PRICING|FLOW|COMPANY))',
    '',
    text,
    flags=re.DOTALL,
)

# 3c) フッターの「お知らせ」リンクを削除
text = re.sub(r'\s*<li><a href="#news">お知らせ</a></li>', '', text)
text = re.sub(r'\s*<li><a href="news/">お知らせ</a></li>', '', text)

# 3d) CTA FINAL セクションを削除（コーポレートHPでは使わないLPパターン）
text = re.sub(
    r'<!-- =+\s*\n\s*CTA FINAL.*?(?=<!-- =+\s*\n\s*FOOTER)',
    '',
    text,
    flags=re.DOTALL,
)

# 4) Services cards desc を実テキスト（元サイト準拠）へ
text = text.replace(
    '木造、鉄骨、RC、そして部分解体まで全工種対応。近隣を歩いて挨拶する地道な合意形成と、現場で積み上げた施工管理。「壊す」を雑にしない、それが日和の作法です。',
    '建築リフォームと同時に解体工事業を自社で請け負っております。近隣への挨拶はもちろん、町を汚さないよう、環境への配慮を忘れずに作業を行うよう、職人全員に指導をしております。',
)
text = text.replace(
    '粉じんを外に出さない封じ込め、レベル1〜3 対応、行政手続きの代行まで。500 件超で培った段取りで、住民・労働者・大気の三方向に責任を持ちます。',
    'アスベスト対策を重要な社会問題と捉え、適正な除去・処理を行うとともに、大気汚染防止に努め、環境保全に貢献していきます。作業に従事する従業員と家族の健康を守るため、安全な作業環境作りも行っています。',
)
text = text.replace(
    '創業当初の主事業は塗装でした。だからこそ、外壁の劣化を「見抜く眼」と「適切な材料選定」が私たちの土台。塗り替え、解体前診断、シーリングまで。',
    '塗装の技術だけではなく、外壁の知識も磨き上げようと常に前向きに作業を行っております。日和建設 外壁診断のプロによる診断を、ぜひ一度お試しください。',
)

# X) FLOW セクション全削除（コーポレートHPのトップに工程フローは置かない）
text = re.sub(
    r'<!-- =+\s*\n\s*FLOW.*?(?=<!-- =+\s*\n\s*(?:COMPANY|FAQ|FOOTER))',
    '',
    text,
    flags=re.DOTALL,
)

# X) COMPANY 会社概要ブロック削除（既に /company/profile.html に専用ページあり）
text = re.sub(
    r'<!-- =+\s*\n\s*COMPANY.*?(?=<!-- =+\s*\n\s*(?:FAQ|FOOTER))',
    '',
    text,
    flags=re.DOTALL,
)

# X) FAQ セクション全削除（コーポレートHPでは無い。LPパターン）
text = re.sub(
    r'<!-- =+\s*\n\s*FAQ.*?(?=<!-- =+\s*\n\s*FOOTER)',
    '',
    text,
    flags=re.DOTALL,
)

# X) JSON-LD から FAQPage / HowTo を削除（ページ上にもう存在しない）
text = re.sub(
    r',\s*\{\s*"@type":\s*"FAQPage".*?\}(?=\s*[,\]])',
    '',
    text,
    flags=re.DOTALL,
)
text = re.sub(
    r',\s*\{\s*"@type":\s*"HowTo".*?\}(?=\s*[,\]])',
    '',
    text,
    flags=re.DOTALL,
)

# X) フッターの「FAQ」「料金プラン」「経営理念」など削除済セクションへのリンクを除去
for fragment in [
    r'\s*<li><a href="#faq">FAQ</a></li>',
    r'\s*<li><a href="#flow">[^<]+</a></li>',
    r'\s*<li><a href="#company">[^<]+</a></li>',
    r'\s*<li><a href="#philosophy">[^<]+</a></li>',
    r'\s*<li><a href="#ceo-message">[^<]+</a></li>',
    r'\s*<li><a href="#sustainability">[^<]+</a></li>',
    r'\s*<li><a href="#history">[^<]+</a></li>',
    r'\s*<li><a href="#news">[^<]+</a></li>',
]:
    text = re.sub(fragment, '', text)

# (元の 5) はもう不要になったが、念のため架空テキストの逐一削除を残す
# 5) FAQ セクション全削除（架空Q&A 8問） → 元サイトの実5問へ置換
real_faq = '''<section id="faq" class="section" aria-label="よくあるご質問">
  <div class="container">
    <span class="eyebrow reveal">FAQ</span>
    <h2 class="section-title reveal">よくいただくご質問。</h2>

    <div class="faq-grid reveal">
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false"><span>リサイクル届の対応は可能ですか？</span><span class="faq-icon" aria-hidden="true"></span></button>
        <div class="faq-a"><div class="faq-a__inner">弊社にて対応させていただきます。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false"><span>残土処理および埋め戻しの対応は可能ですか？</span><span class="faq-icon" aria-hidden="true"></span></button>
        <div class="faq-a"><div class="faq-a__inner">対応可能です。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false"><span>石綿（アスベスト）含有調査の対応は可能ですか？</span><span class="faq-icon" aria-hidden="true"></span></button>
        <div class="faq-a"><div class="faq-a__inner">石綿検体の採取および含有調査、対応させていただきます。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false"><span>見積りしてもらうだけになってもいいですか？</span><span class="faq-icon" aria-hidden="true"></span></button>
        <div class="faq-a"><div class="faq-a__inner">お見積もりだけでも大歓迎です（無料）。案件以外の不動産業の方のご相談も常に対応しています。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false"><span>解体業の方は無愛想なイメージがありますが…</span><span class="faq-icon" aria-hidden="true"></span></button>
        <div class="faq-a"><div class="faq-a__inner">弊社では、解体業のイメージを変えるため、作業員にも理念を共有しています。小さな心がけから印象を変えていけるように心がけています。</div></div>
      </div>
    </div>
  </div>
</section>'''
text = re.sub(
    r'<section id="faq".*?</section>',
    real_faq,
    text,
    count=1,
    flags=re.DOTALL,
)

# 4) ABOUT teaser: 経営理念カード → 代表挨拶カード
text = text.replace(
    '<img src="assets/img/services/demolition.webp" alt="経営理念" loading="lazy" />',
    '<img src="assets/img/reasons/supervisor.webp" alt="代表挨拶" loading="lazy" />',
)
text = text.replace(
    '<span class="card-service__num">PHILOSOPHY</span>\n          <h3 class="card-service__title">経営理念<small>OUR PHILOSOPHY</small></h3>\n          <p class="card-service__desc">建物への敬意、近隣への配慮、仕事への誠実 ─ 日和建設が掲げる三つの価値観をご紹介します。</p>',
    '<span class="card-service__num">MESSAGE</span>\n          <h3 class="card-service__title">代表挨拶<small>FROM CEO</small></h3>\n          <p class="card-service__desc">代表取締役 吉田 光輝より、日和建設の理念「平和」と、解体・アスベスト除去工事への取り組み姿勢をお伝えします。</p>',
)
text = text.replace(
    'href="company/philosophy.html">経営理念を見る',
    'href="company/message.html">代表挨拶を見る',
)

# 5) ABOUT teaser: 2枚目のMESSAGEカードと重複するので、2枚目を「沿革」へ差し替え
text = text.replace(
    '<img src="assets/img/reasons/supervisor.webp" alt="代表メッセージ" loading="lazy" />',
    '<img src="assets/img/services/demolition.webp" alt="沿革" loading="lazy" />',
)
text = text.replace(
    '<span class="card-service__num">MESSAGE</span>\n          <h3 class="card-service__title">代表メッセージ<small>FROM CEO</small></h3>\n          <p class="card-service__desc">代表取締役 吉田 光輝より、創業の背景と「晴れた日のような仕事」への想いをお伝えします。</p>\n          <span class="card-service__bar" aria-hidden="true"></span>\n          <a class="btn-link card-service__link" href="company/message.html">代表メッセージを見る</a>',
    '<span class="card-service__num">HISTORY</span>\n          <h3 class="card-service__title">沿革<small>OUR HISTORY</small></h3>\n          <p class="card-service__desc">2017年のアスベスト除去業・塗装業開始から、2021年の株式会社 日和建設 設立まで。事業領域を一歩ずつ広げてきた歩みです。</p>\n          <span class="card-service__bar" aria-hidden="true"></span>\n          <a class="btn-link card-service__link" href="company/history.html">沿革を見る</a>',
)

# 6) ABOUT lede 書き換え: "1,000 を超える現場" を削除し、実際の事業範囲に置換
text = text.replace(
    '<p class="section-lede reveal">解体は、街が次の姿になるための前工程。だからこそ、騒音・粉じん・近隣との関係性まで、ひとつずつ丁寧に整える仕事に徹してきました。創業以来、堺の街で 1,000 を超える現場に立ち会い、その都度学び、磨いてきた作法があります。</p>',
    '<p class="section-lede reveal">日和建設の理念は「平和」── 騙し合い、いじめ、環境破壊、迷惑のない平和な事業をめざしています。2017年の外壁・塗装事業から始まり、解体・アスベスト除去まで、建物の一生に幅広く関わってきました。</p>',
)

# 7) HERO 直下の sub 書き換え（"街が次の姿になるための、はじまりの工程です" は OK だが念のため確認のみ）

# 8) ABOUT 見出し書き換え: "壊すだけでは、終わらない。" → 元サイト寄りの "解体工事のイメージをクリーンに。"
text = text.replace(
    '<h2 class="section-title reveal">壊すだけでは、終わらない。</h2>',
    '<h2 class="section-title reveal">解体工事のイメージを、<br />クリーンに。</h2>',
)

INDEX.write_text(text, encoding="utf-8")
print(f"[OK] index.html {original_len:,} → {len(text):,} bytes ({len(text) - original_len:+,})")

# Verify nothing fake remains
issues = []
for pattern, name in [
    (r'data-target="1000"', 'fake KPI 1000'),
    (r'data-target="500"', 'fake KPI 500'),
    (r'data-target="300"', 'fake KPI 300'),
    (r'sustain-card', 'fake sustainability cards'),
    (r'href="strengths/"', 'broken strengths link'),
    (r'href="sustainability/"', 'broken sustainability link'),
    (r'href="culture/"', 'broken culture link'),
    (r'href="blog/"', 'broken blog link'),
    (r'philosophy\.html', 'deleted philosophy link'),
    (r'reason__num', 'fake 4 reasons block'),
]:
    if re.search(pattern, text):
        issues.append(f"  ✗ still found: {name}")
if issues:
    print("\nREMAINING ISSUES:")
    for i in issues: print(i)
else:
    print("\n[CLEAN] no fake content references remain in index.html")
