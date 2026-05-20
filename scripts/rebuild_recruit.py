#!/usr/bin/env python3
"""
recruit.html を元サイト /job-offer/ の実求人データで再構築。

元サイト掲載の4職種:
- 解体作業員       日給11,000~16,000円
- ダンプトラック運転手兼作業 日給13,000~16,000円
- 重機オペレーター 日給13,000~18,000円
- 営業             月給25万円~35万円

共通条件（解体系3職種）:
- 勤務時間 8:00-17:00（本社7:00集合）
- 休日   祝日・日曜
- 福利厚生 交通費一部支給
- 未経験OK / 週2日OK / 平日・土日OK / 中型免許優遇

実行: python3 scripts/rebuild_recruit.py
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from generate_section_pages import HEADER, FOOTER, head, page_hero, breadcrumb_inline

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "recruit.html"


def job_card(num, num_en, title, title_en, salary, hours, notes_html):
    return f'''      <article class="card-service">
        <div class="card-service__body" style="padding-top:48px;">
          <span class="card-service__num">{num} ／ {num_en}</span>
          <h3 class="card-service__title">{title}<small>{title_en}</small></h3>
          <div style="margin-top:16px; padding:20px 0; border-top:1px solid var(--c-line-dark); border-bottom:1px solid var(--c-line-dark);">
            <p style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); margin-bottom:8px;">SALARY</p>
            <p style="font-size:18px; line-height:1.6;">{salary}</p>
            <p style="font-family:var(--ff-sans-en); font-size:11px; letter-spacing:.24em; color:var(--c-brass); margin: 16px 0 8px;">HOURS</p>
            <p style="font-size:14px; line-height:1.8;">{hours}</p>
          </div>
          <p class="card-service__desc" style="margin-top:16px;">{notes_html}</p>
          <span class="card-service__bar" aria-hidden="true"></span>
        </div>
      </article>'''


COMMON_NOTES = (
    "祝日・日曜休み／交通費一部支給。スタッフの平均収入 35〜45 万円。"
    "未経験でも大歓迎、週2日勤務から OK。平日・土日のみ勤務も可能。"
    "中型免許をお持ちの方は優遇、別途手当あり。"
)

JOBS = [
    {
        "num": "JOB 01", "num_en": "DEMOLITION", "title": "解体作業員",
        "title_en": "DISMANTLING WORKER",
        "salary": "日給 11,000 〜 16,000 円",
        "hours": "8:00 〜 17:00（本社 7:00 集合）",
        "notes": COMMON_NOTES,
    },
    {
        "num": "JOB 02", "num_en": "DUMP DRIVER", "title": "ダンプトラック運転手 兼 作業員",
        "title_en": "DUMP TRUCK DRIVER",
        "salary": "日給 13,000 〜 16,000 円",
        "hours": "8:00 〜 17:00（本社 7:00 集合）",
        "notes": COMMON_NOTES,
    },
    {
        "num": "JOB 03", "num_en": "HEAVY MACHINERY", "title": "重機オペレーター",
        "title_en": "HEAVY MACHINERY OPERATOR",
        "salary": "日給 13,000 〜 18,000 円",
        "hours": "8:00 〜 17:00（本社 7:00 集合）",
        "notes": COMMON_NOTES,
    },
    {
        "num": "JOB 04", "num_en": "SALES", "title": "営業",
        "title_en": "SALES",
        "salary": "月給 25 〜 35 万円",
        "hours": "9:00 〜 17:00",
        "notes": (
            "祝日・日曜・その他月 2 回休み／交通費一部支給／オフィスカジュアル可。"
            "解体・不動産・建設会社への法人営業。ノルマ（1日 ●件 必達 等）は設けておりません。"
        ),
    },
]


BODY = f'''<section class="section">
  <div class="container">
    <div style="max-width:780px;">
      <p class="section-lede reveal" style="font-size:17px; line-height:2.2;">日和建設では、解体・アスベスト除去・塗装の現場を支えるメンバーを募集しています。未経験から始めて資格を取り、長く働ける環境をつくるのが、私たちの方針です。</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow reveal">OPEN POSITIONS</span>
    <h2 class="section-title reveal">募集職種。</h2>

    <div class="services-grid reveal-stagger" style="margin-top:64px;">
''' + "\n".join(job_card(j["num"], j["num_en"], j["title"], j["title_en"], j["salary"], j["hours"], j["notes"]) for j in JOBS) + '''
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container">
    <span class="eyebrow reveal">CONDITIONS</span>
    <h2 class="section-title reveal">共通条件・福利厚生。</h2>

    <div style="margin-top:48px;">
      <table class="company-table" style="width:100%;">
        <tbody>
          <tr><th>勤務地</th><td>大阪府堺市東区（本社）／ 南大阪営業所 ／ 東京営業所 ／ 各現場</td></tr>
          <tr><th>休日</th><td>祝日・日曜（営業職はその他月2回）</td></tr>
          <tr><th>福利厚生</th><td>交通費一部支給</td></tr>
          <tr><th>勤務時間</th><td>解体系：8:00〜17:00（本社 7:00 集合）／ 営業：9:00〜17:00</td></tr>
          <tr><th>未経験者</th><td>大歓迎（解体・廃材撤去の現場内容により給与は変動）</td></tr>
          <tr><th>スタッフ平均収入</th><td>35〜45 万円</td></tr>
          <tr><th>その他</th><td>中型免許優遇／週2日勤務OK／平日・土日のみOK／シフト調整可／天候による急遽休みあり／基本残業なし／早く終わっても日給に変動なし</td></tr>
        </tbody>
      </table>
    </div>

    <p style="margin-top:48px; font-size:14px; color: var(--c-text-mute); line-height:2;">※ 出来次第で随時昇給。<br />※ 現場によって直行直帰の場合あり。<br />※ 友達と同じシフトでの勤務も歓迎します。</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow reveal">APPLY</span>
    <h2 class="section-title reveal">ご応募・お問い合わせ。</h2>
    <p class="section-lede reveal">採用に関するお問い合わせは、お問い合わせフォームよりご連絡ください。</p>
    <p style="margin-top:32px;"><a class="btn-link" href="contact.html">お問い合わせフォームへ</a></p>
  </div>
</section>
'''


def main():
    bc = breadcrumb_inline([("ホーム", "index.html"), ("採用情報", "")])
    html = head(
        "採用情報｜株式会社 日和建設",
        "解体作業員・ダンプトラック運転手・重機オペレーター・営業の4職種を募集。日給11,000円〜、未経験歓迎、週2日勤務OK。",
        "https://nichiwa-kensetu.com/recruit.html",
        "/assets/img/services/demolition.webp",
    )
    html += HEADER + "\n"
    html += page_hero(
        "採用情報", "RECRUIT",
        "仲間を、募集しています。",
        "Recruit",
        "解体・アスベスト除去・塗装の現場を支えるメンバーを募集しています。未経験から始めて資格を取り、長く働ける環境をつくるのが、私たちの方針です。",
        "assets/img/services/demolition.webp",
        bc,
    )
    html += BODY
    html += FOOTER
    html += "\n</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"✓ recruit.html ({len(html)} bytes)")


if __name__ == "__main__":
    main()
