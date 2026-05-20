#!/usr/bin/env python3
"""
docs/index.html を recruit.co.jp ホームページ形式に再構築。

LP的な「全部1ページに詰め込み」から、各セクションは「teaser + 詳細ページへのリンク」へ。
削除/縮約: PHILOSOPHY, CEO_MESSAGE, WHY, VOICES, HISTORY, COMPANY, FAQ
保持: HERO, KPI, SERVICES, WORKS, SUSTAINABILITY, NEWS, PRICING, FLOW, CTA_FINAL

実行: python3 scripts/rebuild_index.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"

# Each tuple: (section_marker_keyword, replacement_html_or_None)
# None = delete entirely (no replacement)
SECTION_REPLACEMENTS = {}

# PHILOSOPHY → "About" teaser block linking to /company/ and /company/philosophy/
SECTION_REPLACEMENTS["PHILOSOPHY"] = '''<section id="about" class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">ABOUT NICHIWA</span>
    <h2 class="section-title reveal">壊すだけでは、終わらない。</h2>
    <p class="section-lede reveal">解体は、街が次の姿になるための前工程。だからこそ、騒音・粉じん・近隣との関係性まで、ひとつずつ丁寧に整える仕事に徹してきました。創業以来、堺の街で 1,000 を超える現場に立ち会い、その都度学び、磨いてきた作法があります。</p>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__media">
          <img src="assets/img/services/demolition.webp" alt="経営理念" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">PHILOSOPHY</span>
          <h3 class="card-service__title">経営理念<small>OUR PHILOSOPHY</small></h3>
          <p class="card-service__desc">建物への敬意、近隣への配慮、仕事への誠実 ─ 日和建設が掲げる三つの価値観をご紹介します。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="company/philosophy.html">経営理念を見る</a>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__media">
          <img src="assets/img/reasons/supervisor.webp" alt="代表メッセージ" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">MESSAGE</span>
          <h3 class="card-service__title">代表メッセージ<small>FROM CEO</small></h3>
          <p class="card-service__desc">代表取締役 吉田 光輝より、創業の背景と「晴れた日のような仕事」への想いをお伝えします。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="company/message.html">代表メッセージを見る</a>
        </div>
      </article>
      <article class="card-service" style="background: var(--c-navy); color: var(--c-off);">
        <div class="card-service__media">
          <img src="assets/img/services/coating.webp" alt="会社概要" loading="lazy" />
        </div>
        <div class="card-service__body">
          <span class="card-service__num">PROFILE</span>
          <h3 class="card-service__title">企業情報<small>COMPANY</small></h3>
          <p class="card-service__desc">商号・所在地・許認可・資本金・従業員数、沿革・許可・資格まで。日和建設の基本情報。</p>
          <span class="card-service__bar" aria-hidden="true"></span>
          <a class="btn-link card-service__link" href="company/">企業情報を見る</a>
        </div>
      </article>
    </div>
  </div>
</section>
'''

# CEO MESSAGE → remove entirely (linked from PHILOSOPHY teaser above)
SECTION_REPLACEMENTS["CEO MESSAGE - 代表メッセージ"] = None

# WHY → teaser linking to /strengths/
SECTION_REPLACEMENTS["WHY - 選ばれる理由"] = '''<section id="why" class="section section--paper" aria-label="選ばれる理由">
  <div class="container">
    <span class="eyebrow reveal">WHY NICHIWA</span>
    <h2 class="section-title reveal">「早い・安い・高品質」では、<br />語り尽くせない、4つの理由。</h2>
    <p class="section-lede reveal">競合と同じ言葉で語ることをやめました。私たちが本当に大切にしてきた4つの軸を、正直にお伝えします。</p>

    <div style="margin-top:48px; display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:24px;">
      <div class="reason"><span class="reason__num">No. 01</span><h3 class="reason__title">近隣との合意形成は、契約より先に。</h3></div>
      <div class="reason"><span class="reason__num">No. 02</span><h3 class="reason__title">解体に「外壁を読む眼」を。</h3></div>
      <div class="reason"><span class="reason__num">No. 03</span><h3 class="reason__title">外部に粉じんを舞わせない最後まで。</h3></div>
      <div class="reason"><span class="reason__num">No. 04</span><h3 class="reason__title">即日対応を、形だけにしない。</h3></div>
    </div>
    <div style="margin-top:48px; text-align:center;">
      <a class="btn-link" href="strengths/">4つの理由を詳しく見る</a>
    </div>
  </div>
</section>
'''

# VOICES → remove entirely (move to /strengths/)
SECTION_REPLACEMENTS["VOICES - お客様の声"] = None

# HISTORY → remove (linked from /company/)
SECTION_REPLACEMENTS["HISTORY - 沿革"] = None

# COMPANY → small summary teaser linking to /company/profile.html
SECTION_REPLACEMENTS["COMPANY - 会社概要"] = '''<section id="company" class="section section--navy" aria-label="会社概要">
  <div class="container">
    <span class="eyebrow reveal">COMPANY PROFILE</span>
    <h2 class="section-title reveal">堺で生まれた、誠実な仕事のこと。</h2>
    <p class="section-lede reveal">2021年7月、堺の事務所5名でのスタート。創業から 4 年で、解体実績1,000件・アスベスト除去500件を積み上げてまいりました。</p>

    <div style="margin-top:48px; display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:32px;">
      <div><strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">商号 ／ NAME</strong><p style="margin-top:8px;">株式会社 日和建設</p></div>
      <div><strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">設立 ／ FOUNDED</strong><p style="margin-top:8px;">2021年 7月 2日</p></div>
      <div><strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">代表 ／ CEO</strong><p style="margin-top:8px;">吉田 光輝</p></div>
      <div><strong style="color:var(--c-brass); font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em;">許可 ／ LICENSE</strong><p style="margin-top:8px;">大阪府知事 解体業許可<br/>第 1494 号</p></div>
    </div>

    <div style="margin-top:48px; display:flex; gap:24px; flex-wrap:wrap;">
      <a class="btn-link" href="company/profile.html">会社概要を詳しく見る</a>
      <a class="btn-link" href="company/history.html">沿革・歴史を見る</a>
      <a class="btn-link" href="company/license.html">許可・資格を見る</a>
    </div>
  </div>
</section>
'''

# FAQ → shorten to top 4 + link to detail
SECTION_REPLACEMENTS["FAQ"] = '''<section id="faq" class="section" aria-label="よくあるご質問">
  <div class="container">
    <span class="eyebrow reveal">FAQ</span>
    <h2 class="section-title reveal">よく寄せられるご質問。</h2>

    <div class="faq-grid reveal">
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false">
          <span>見積りは無料ですか？</span>
          <span class="faq-icon" aria-hidden="true"></span>
        </button>
        <div class="faq-a"><div class="faq-a__inner">現地調査・お見積りは完全無料です。出張費もいただきません。大阪・兵庫・京都・奈良・和歌山、東京近郊にも対応します。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false">
          <span>アスベストの有無が分からないのですが、調べてもらえますか？</span>
          <span class="faq-icon" aria-hidden="true"></span>
        </button>
        <div class="faq-a"><div class="faq-a__inner">はい。建材サンプル採取と分析機関への依頼までお手伝いします。レベル 1 〜 3 いずれも対応可能です。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false">
          <span>着工までどれくらいかかりますか？</span>
          <span class="faq-icon" aria-hidden="true"></span>
        </button>
        <div class="faq-a"><div class="faq-a__inner">お問い合わせから最短 2 週間で着工可能です。アスベスト届出が必要な現場は、行政手続き期間が加わります。</div></div>
      </div>
      <div class="faq-item">
        <button type="button" class="faq-q" aria-expanded="false">
          <span>近隣への挨拶はどこまでやってくれますか？</span>
          <span class="faq-icon" aria-hidden="true"></span>
        </button>
        <div class="faq-a"><div class="faq-a__inner">30m 圏（マンションは上下左右含む）への直接訪問を標準とし、ご不在宅にはご挨拶状を投函します。</div></div>
      </div>
    </div>
  </div>
</section>
'''


def replace_section(text: str, keyword: str, replacement: str | None) -> str:
    """
    Replace a section identified by its HTML comment marker.
    Section start: '<!-- ====== KEYWORD ====== -->' (with possible variations)
    Section end: the next '<!-- ====== ' comment OR </section> closing.
    """
    # Find the section start comment containing the keyword
    pattern = re.compile(
        r'(<!-- =+\s*\n\s*' + re.escape(keyword) + r'.*?-->\s*)(.*?)(?=<!-- =+|\Z)',
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        print(f"  ✗ {keyword}: section marker not found")
        return text
    if replacement is None:
        # Delete entirely (including the comment marker)
        new = text[:m.start()] + text[m.end():]
    else:
        # Keep the comment marker, replace the body
        new = text[:m.start()] + m.group(1) + replacement + "\n\n" + text[m.end():]
    print(f"  ✓ {keyword}: {'removed' if replacement is None else 'replaced'}")
    return new


def main():
    text = INDEX.read_text(encoding="utf-8")
    original_len = len(text)
    for keyword, replacement in SECTION_REPLACEMENTS.items():
        text = replace_section(text, keyword, replacement)
    INDEX.write_text(text, encoding="utf-8")
    print(f"\n[OK] {original_len:,} → {len(text):,} bytes ({len(text) - original_len:+,})")


if __name__ == "__main__":
    main()
