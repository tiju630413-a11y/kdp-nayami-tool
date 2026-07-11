#!/usr/bin/env python3
"""KDP レポート取込（売上・KENP CSV → data/performance.db。仕様 §5 工程9）。

KDP に売上APIは無いため、ダッシュボードからDLしたレポート（CSV）を取り込む。
レポートの列名はKDPの仕様変更で揺れるため、--col-* で上書きできる（D-12）。

使い方:
  python3 scripts/import_kdp.py sales <csvファイル>   # 注文・ロイヤリティ
  python3 scripts/import_kdp.py kenp <csvファイル>    # KENP既読ページ
  python3 scripts/import_kdp.py review <NNN> --stars 4 --text "..." [--date YYYY-MM-DD]
  python3 scripts/import_kdp.py register <NNN>        # 出版した本をDBに登録
  python3 scripts/import_kdp.py show                  # 取込済みデータの要約

初回実行時にDBとスキーマを自動作成する。
"""
import argparse
import csv
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, find_book

DB = ROOT / "data" / "performance.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
  book_id TEXT PRIMARY KEY,      -- books/ のディレクトリ名（例 001_iikaesenai）
  asin TEXT,
  title TEXT,
  series TEXT,
  genre_id TEXT,                 -- genre_map の W-XXXX
  published_on TEXT,
  price_yen INTEGER
);
CREATE TABLE IF NOT EXISTS sales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  asin TEXT,
  title TEXT,
  units INTEGER DEFAULT 0,
  royalty REAL DEFAULT 0,
  kenp INTEGER DEFAULT 0,
  source_file TEXT,
  UNIQUE(date, asin, source_file)
);
CREATE TABLE IF NOT EXISTS reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT,
  date TEXT,
  stars INTEGER,
  text TEXT
);
CREATE TABLE IF NOT EXISTS retro_weekly (
  week TEXT PRIMARY KEY,         -- 2026-W28
  readthrough_min_per_book REAL, -- 通読所要時間（分/冊）
  image_min_per_book REAL,       -- 画像作業時間（分/冊）
  model_quota_pct REAL,          -- モデル枠消費率(%)
  fixes_at_readthrough INTEGER,  -- 通読での修正数（0=一発OK）
  notes TEXT
);
"""


def db():
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    return conn


def import_csv(kind, path, args):
    """sales: 日付/ASIN/タイトル/冊数/ロイヤリティ, kenp: 日付/ASIN/タイトル/KENP"""
    conn = db()
    cols = {
        "date": args.col_date, "asin": args.col_asin, "title": args.col_title,
        "units": args.col_units, "royalty": args.col_royalty, "kenp": args.col_kenp,
    }
    n = 0
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        def pick(row, want, cands):
            if cols[want] and cols[want] in row:
                return row[cols[want]]
            for c in cands:
                for h in headers:
                    if c.lower() in h.lower():
                        return row[h]
            return ""

        for row in reader:
            d = pick(row, "date", ["date", "日付"]) or date.today().isoformat()
            asin = pick(row, "asin", ["asin"])
            title = pick(row, "title", ["title", "タイトル"])
            units = royalty = kenp = 0
            if kind == "sales":
                units = _num(pick(row, "units", ["units", "net", "注文", "販売"]))
                royalty = _num(pick(row, "royalty", ["royalty", "ロイヤリティ"]), float)
            else:
                kenp = _num(pick(row, "kenp", ["kenp", "pages", "ページ"]))
            try:
                conn.execute(
                    "INSERT INTO sales(date, asin, title, units, royalty, kenp, source_file)"
                    " VALUES (?,?,?,?,?,?,?)",
                    (d[:10], asin, title, units, royalty, kenp, Path(path).name))
                n += 1
            except sqlite3.IntegrityError:
                pass  # 同一ファイル再取込はスキップ（冪等）
    conn.commit()
    print(f"取込: {n}行（{kind} / {Path(path).name}）")


def _num(v, cast=int):
    try:
        return cast(str(v).replace(",", "").strip() or 0)
    except ValueError:
        return 0


def cmd_register(nnn):
    book = find_book(nnn)
    meta = json.loads((book / "book.json").read_text(encoding="utf-8"))
    plan = (book / "plan.md").read_text(encoding="utf-8") if (book / "plan.md").exists() else ""
    import re
    gm = re.search(r"W-\d{4}", plan)
    conn = db()
    conn.execute(
        "INSERT OR REPLACE INTO books(book_id, asin, title, series, genre_id,"
        " published_on, price_yen) VALUES (?,?,?,?,?,?,?)",
        (book.name, meta.get("asin", ""), meta["title"], meta.get("series_name", ""),
         gm.group(0) if gm else "", meta.get("publish_date") or date.today().isoformat(),
         500))
    conn.commit()
    print(f"登録: {book.name} / {meta['title']}")
    print("ASIN確定後: book.json に asin を書いて再実行（上書き登録）")


def cmd_review(nnn, args):
    book = find_book(nnn)
    conn = db()
    conn.execute("INSERT INTO reviews(book_id, date, stars, text) VALUES (?,?,?,?)",
                 (book.name, args.date or date.today().isoformat(), args.stars,
                  args.text or ""))
    conn.commit()
    print(f"レビュー記録: {book.name} ★{args.stars}")


def cmd_show():
    conn = db()
    for label, q in [
        ("書籍", "SELECT COUNT(*) FROM books"),
        ("売上行", "SELECT COUNT(*) FROM sales"),
        ("販売冊数計", "SELECT COALESCE(SUM(units),0) FROM sales"),
        ("ロイヤリティ計", "SELECT ROUND(COALESCE(SUM(royalty),0)) FROM sales"),
        ("KENP計", "SELECT COALESCE(SUM(kenp),0) FROM sales"),
        ("レビュー", "SELECT COUNT(*) FROM reviews"),
    ]:
        print(f"{label}: {conn.execute(q).fetchone()[0]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["sales", "kenp", "review", "register", "show"])
    ap.add_argument("target", nargs="?", help="CSVパス（sales/kenp）または NNN（review/register）")
    ap.add_argument("--stars", type=int, choices=range(1, 6))
    ap.add_argument("--text", default="")
    ap.add_argument("--date")
    for c in ("date", "asin", "title", "units", "royalty", "kenp"):
        ap.add_argument(f"--col-{c}", dest=f"col_{c}", help=f"CSVの{c}列名を明示指定")
    args = ap.parse_args()

    if args.command == "show":
        return cmd_show()
    if not args.target:
        ap.error("target が必要")
    if args.command in ("sales", "kenp"):
        return import_csv(args.command, args.target, args)
    if args.command == "register":
        return cmd_register(args.target)
    if args.command == "review":
        if not args.stars:
            ap.error("--stars 1-5 が必要")
        return cmd_review(args.target, args)


if __name__ == "__main__":
    sys.exit(main() or 0)
