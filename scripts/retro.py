#!/usr/bin/env python3
"""週次レトロ生成（仕様 §5 工程9）。

KPI集計を logs/retro_YYYY-Www.md に出力する。解釈と意思決定は
prompts/09_retro.md を実行するモデルの仕事（このスクリプトは数字のみ）。

使い方:
  python3 scripts/retro.py                 # 今週のレトロ集計を生成
  python3 scripts/retro.py --week 2026-W28 # 対象週を指定
  python3 scripts/retro.py --summary       # plan 工程向けの短い要約を標準出力
  python3 scripts/retro.py log --readthrough-min 95 --image-min 40 \
      --quota-pct 30 --fixes 0 [--notes "..."]   # 今週のスループット実測を記録
"""
import argparse
import json
import sqlite3
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, load_settings, load_assets

DB = ROOT / "data" / "performance.db"


def iso_week(d=None):
    d = d or date.today()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def week_range(week):
    y, w = int(week[:4]), int(week[6:])
    start = datetime.fromisocalendar(y, w, 1).date()
    return start, start + timedelta(days=6)


def conn_or_none():
    if not DB.exists():
        return None
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def asset_pool_stats(cfg):
    assets = load_assets()
    reuse_cap = cfg["max_asset_reuse"]
    available = [a for a in assets if len(a.get("used_in", [])) < reuse_cap]
    exhausted = len(assets) - len(available)
    by_tag = Counter(t for a in available for t in a.get("tags", []))
    per_book = cfg["min_author_assets"]
    # 残り採用可能スロット（各資産は reuse_cap - used 回使える）
    slots = sum(reuse_cap - len(a.get("used_in", [])) for a in available)
    books_left = slots // per_book if per_book else 0
    return {
        "total": len(assets), "available": len(available), "exhausted": exhausted,
        "slots": slots, "books_left": books_left,
        "top_tags": by_tag.most_common(5),
    }


def collect(week, cfg):
    start, end = week_range(week)
    c = conn_or_none()
    data = {"week": week, "start": str(start), "end": str(end),
            "sales_week": 0, "royalty_week": 0.0, "kenp_week": 0,
            "royalty_month": 0.0, "reviews": [], "by_title": [],
            "throughput": None, "published_total": 0}
    if c:
        row = c.execute(
            "SELECT COALESCE(SUM(units),0) u, COALESCE(SUM(royalty),0) r,"
            " COALESCE(SUM(kenp),0) k FROM sales WHERE date BETWEEN ? AND ?",
            (str(start), str(end))).fetchone()
        data.update(sales_week=row["u"], royalty_week=row["r"], kenp_week=row["k"])
        month = str(end)[:7]  # 週の終了日（日曜レトロ実行日側）の月を「今月」とする
        data["royalty_month"] = c.execute(
            "SELECT COALESCE(SUM(royalty),0) FROM sales WHERE date LIKE ?",
            (month + "%",)).fetchone()[0]
        data["by_title"] = [dict(r) for r in c.execute(
            "SELECT title, SUM(units) units, SUM(kenp) kenp, ROUND(SUM(royalty)) royalty"
            " FROM sales WHERE date BETWEEN ? AND ? GROUP BY title ORDER BY royalty DESC",
            (str(start), str(end)))]
        data["reviews"] = [dict(r) for r in c.execute(
            "SELECT book_id, date, stars FROM reviews WHERE date BETWEEN ? AND ?",
            (str(start), str(end)))]
        data["published_total"] = c.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        t = c.execute("SELECT * FROM retro_weekly WHERE week=?", (week,)).fetchone()
        data["throughput"] = dict(t) if t else None
    data["assets"] = asset_pool_stats(cfg)
    return data


def render(d, cfg):
    a = d["assets"]
    t = d["throughput"]
    target = cfg["target_monthly_revenue"]
    pace = cfg["pace_per_week"]
    lines = [
        f"# 週次レトロ集計: {d['week']}（{d['start']}〜{d['end']}）",
        "",
        "数字の集計のみ。解釈・倍賭け/撤退・翌週ペースの決定は prompts/09_retro.md を実行。",
        "",
        "## 売上KPI",
        "",
        f"- 今週: 販売 {d['sales_week']} 冊 / KENP {d['kenp_week']:,} / "
        f"ロイヤリティ ¥{d['royalty_week']:,.0f}",
        f"- 今月累計ロイヤリティ: ¥{d['royalty_month']:,.0f}"
        f"（目標 ¥{target:,} / 進捗 {100 * d['royalty_month'] / target:.1f}%）",
        f"- 出版済み: {d['published_total']} 冊",
        "",
        "### タイトル別（今週）",
        "",
        "| タイトル | 冊数 | KENP | ロイヤリティ |",
        "|---|---|---|---|",
    ]
    lines += [f"| {r['title']} | {r['units']} | {r['kenp']} | ¥{r['royalty']} |"
              for r in d["by_title"]] or ["| （データなし） | | | |"]
    lines += ["", "### レビュー（今週）", ""]
    if d["reviews"]:
        lines += [f"- {r['book_id']} ★{r['stars']}（{r['date']}）" for r in d["reviews"]]
    else:
        lines += ["- なし"]
    lines += [
        "",
        "## スループット実測（律速3指標＋一発OK）",
        "",
    ]
    if t:
        lines += [
            f"- 通読所要時間: {t['readthrough_min_per_book']} 分/冊 → "
            f"週{pace}冊で {t['readthrough_min_per_book'] * pace / 60:.1f} 時間",
            f"- 画像作業時間: {t['image_min_per_book']} 分/冊",
            f"- モデル枠消費: {t['model_quota_pct']}%",
            f"- 通読での修正数: {t['fixes_at_readthrough']}"
            f"（{'一発OK達成' if t['fixes_at_readthrough'] == 0 else '要還流（未還流なら翌週着手ブロック）'}）",
        ]
        if t.get("notes"):
            lines.append(f"- メモ: {t['notes']}")
    else:
        lines += ["- 未記録。`python3 scripts/retro.py log --readthrough-min N "
                  "--image-min N --quota-pct N --fixes N` で記録する"]
    lines += [
        "",
        "## 著者資産プール",
        "",
        f"- 総数 {a['total']} / 採用可能 {a['available']}"
        f"（再利用上限到達 {a['exhausted']}件）",
        f"- 採用可能スロット {a['slots']} → **あと約 {a['books_left']} 冊分**"
        f"（1冊 {cfg['min_author_assets']} 件消費・上限 {cfg['max_asset_reuse']} 冊/資産）",
        f"- 週次補充目標: {cfg['weekly_asset_intake_target']} 件",
        f"- タグ上位: " + (", ".join(f"{k}({v})" for k, v in a["top_tags"]) or "なし"),
        "",
        f"## 現在の設定: pace_per_week={pace} / 収益目標 ¥{target:,}/月",
    ]
    return "\n".join(lines) + "\n"


def cmd_log(args, week):
    conn = sqlite3.connect(DB)
    conn.executescript("""CREATE TABLE IF NOT EXISTS retro_weekly (
      week TEXT PRIMARY KEY, readthrough_min_per_book REAL, image_min_per_book REAL,
      model_quota_pct REAL, fixes_at_readthrough INTEGER, notes TEXT);""")
    conn.execute(
        "INSERT OR REPLACE INTO retro_weekly VALUES (?,?,?,?,?,?)",
        (week, args.readthrough_min, args.image_min, args.quota_pct,
         args.fixes, args.notes))
    conn.commit()
    print(f"記録: {week} 通読{args.readthrough_min}分 画像{args.image_min}分 "
          f"枠{args.quota_pct}% 修正{args.fixes}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", default="report", choices=["report", "log"])
    ap.add_argument("--week", default=iso_week())
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--readthrough-min", type=float, default=0)
    ap.add_argument("--image-min", type=float, default=0)
    ap.add_argument("--quota-pct", type=float, default=0)
    ap.add_argument("--fixes", type=int, default=0)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    cfg = load_settings()
    if args.command == "log":
        return cmd_log(args, args.week)

    d = collect(args.week, cfg)
    if args.summary:
        a = d["assets"]
        print(f"今月ロイヤリティ ¥{d['royalty_month']:,.0f} / 目標比 "
              f"{100 * d['royalty_month'] / cfg['target_monthly_revenue']:.0f}% | "
              f"資産プール: 採用可能{a['available']}件・あと約{a['books_left']}冊分 | "
              f"出版済み{d['published_total']}冊")
        return 0
    out = ROOT / "logs" / f"retro_{d['week']}.md"
    out.write_text(render(d, cfg), encoding="utf-8")
    print(f"生成: {out.relative_to(ROOT)}")
    print("次: prompts/09_retro.md を実行して意思決定（倍賭け/撤退・翌週ペース）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
