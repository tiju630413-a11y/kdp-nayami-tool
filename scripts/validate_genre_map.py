#!/usr/bin/env python3
"""genre_map の統合と整合性検証（仕様 §4.1 の自己検証パス）。

data/genre_map_parts/*.json を統合して data/genre_map.json を生成し、
重複・粒度・大分類バランス・スキーマ・参照整合を検証して
logs/genre_map_validation.md にレポートを書く。

再実行可能: エントリを追加・修正したら parts を直して再実行する。
使い方: python3 scripts/validate_genre_map.py
終了コード: 0=PASS(WARNのみ含む) / 1=FAIL あり
"""
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS_DIR = ROOT / "data" / "genre_map_parts"
OUT = ROOT / "data" / "genre_map.json"
LOG = ROOT / "logs" / "genre_map_validation.md"

REQUIRED_FIELDS = {
    "id": str, "category": str, "subcategory": str, "pain": str,
    "reader": str, "severity": int, "evergreen": int, "keywords": list,
    "title_ideas": list, "series_potential": str, "adjacent_ids": list,
    "trend_hooks": list, "notes": str,
}
VALID_SERIES = {"high", "medium", "low"}
# 「読者自身の言葉」から遠い抽象ラベルの兆候
ABSTRACT_PAT = re.compile(r"(に悩んでいる|が課題|問題を抱えて)$")


def load_parts():
    entries, errors = [], []
    for p in sorted(PARTS_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"FAIL: {p.name} がJSONとして不正: {e}")
            continue
        if not isinstance(data, list):
            errors.append(f"FAIL: {p.name} が配列でない")
            continue
        entries.extend(data)
    return entries, errors


def validate(entries):
    fails, warns = [], []
    ids = [e.get("id", "") for e in entries]
    id_set = set(ids)

    # ID重複
    for i, n in Counter(ids).items():
        if n > 1:
            fails.append(f"ID重複: {i} が {n} 回")

    # スキーマ・値域
    for e in entries:
        eid = e.get("id", "?")
        for f, t in REQUIRED_FIELDS.items():
            if f not in e:
                fails.append(f"{eid}: フィールド欠落 {f}")
            elif not isinstance(e[f], t):
                fails.append(f"{eid}: {f} の型が不正（{type(e[f]).__name__}）")
        for f in ("severity", "evergreen"):
            v = e.get(f)
            if isinstance(v, int) and not 1 <= v <= 5:
                fails.append(f"{eid}: {f}={v} が1-5範囲外")
        if e.get("series_potential") not in VALID_SERIES:
            fails.append(f"{eid}: series_potential が不正: {e.get('series_potential')}")
        pain = e.get("pain", "")
        if len(pain) < 25:
            warns.append(f"{eid}: pain が短い（{len(pain)}字）— 粒度不足の疑い: {pain}")
        if len(pain) > 100:
            warns.append(f"{eid}: pain が長い（{len(pain)}字）— 複数悩みの混在の疑い")
        if ABSTRACT_PAT.search(pain):
            warns.append(f"{eid}: pain が抽象ラベル調: {pain}")
        if not e.get("keywords"):
            fails.append(f"{eid}: keywords が空")
        if len(e.get("title_ideas", [])) < 2:
            warns.append(f"{eid}: title_ideas が2案未満")
        # trend_hooks があるのに evergreen 5 は矛盾しないが、逆（時事依存で evergreen 高）を目視できるよう警告
        if e.get("trend_hooks") and e.get("evergreen", 0) >= 5:
            warns.append(f"{eid}: trend_hooks ありで evergreen=5 — 再採点確認")
        # 参照整合
        for a in e.get("adjacent_ids", []):
            if a not in id_set:
                fails.append(f"{eid}: adjacent_ids に存在しないID {a}")
            if a == eid:
                fails.append(f"{eid}: adjacent_ids が自己参照")

    # pain の重複（正規化して比較）
    norm = Counter()
    for e in entries:
        key = re.sub(r"[、。・\s]", "", e.get("pain", ""))
        norm[key] += 1
    for k, n in norm.items():
        if n > 1 and k:
            fails.append(f"pain 完全重複 x{n}: {k[:40]}…")

    return fails, warns


def report(entries, fails, warns, load_errors):
    total = len(entries)
    by_cat = Counter(e["category"] for e in entries if "category" in e)
    by_sub = Counter((e.get("category"), e.get("subcategory")) for e in entries)
    sev = Counter(e.get("severity") for e in entries)
    evg = Counter(e.get("evergreen") for e in entries)

    lines = [
        f"# genre_map 整合性検証ログ（{date.today().isoformat()}）",
        "",
        f"- 総エントリ数: **{total}**（仕様要求 300〜500: "
        f"{'PASS' if 300 <= total <= 500 else 'FAIL'}）",
        f"- FAIL: {len(fails) + len(load_errors)} 件 / WARN: {len(warns)} 件",
        "",
        "## 大分類バランス（10軸）",
        "",
        "| 大分類 | 件数 |",
        "|---|---|",
    ]
    for c, n in by_cat.most_common():
        lines.append(f"| {c} | {n} |")
    mx, mn = (max(by_cat.values()), min(by_cat.values())) if by_cat else (0, 0)
    lines += [
        "",
        f"- カテゴリ数: {len(by_cat)}（期待10）/ 最大最小比: {mx}:{mn}"
        f"（{'PASS' if mn and mx / mn <= 1.5 else 'WARN: 偏りあり'}）",
        f"- 中分類数: {len(by_sub)}（1中分類あたり平均 {total / max(len(by_sub),1):.1f} 件）",
        "",
        "## 採点分布",
        "",
        f"- severity: " + ", ".join(f"{k}: {v}件" for k, v in sorted(sev.items())),
        f"- evergreen: " + ", ".join(f"{k}: {v}件" for k, v in sorted(evg.items())),
        "",
        "## FAIL（出版工程をブロック）",
        "",
    ]
    lines += [f"- {f}" for f in load_errors + fails] or ["- なし"]
    lines += ["", "## WARN（次回の再採点・改稿候補）", ""]
    lines += [f"- {w}" for w in warns] or ["- なし"]
    lines += [
        "",
        "## 検証項目（仕様 §4.1）",
        "",
        "- [x] 重複統合（ID・pain の完全重複チェック）",
        "- [x] 粒度の均し（pain 字数 25〜100 字レンジ検査）",
        "- [x] 大分類間のバランス確認（最大最小比 1.5 以内）",
        "- [x] severity / evergreen の値域・矛盾検査",
        "- [x] adjacent_ids の参照整合",
        "",
        "再実行: `python3 scripts/validate_genre_map.py`（parts 修正後に何度でも）",
    ]
    return "\n".join(lines)


def main():
    entries, load_errors = load_parts()
    fails, warns = validate(entries)
    ok = not fails and not load_errors and 300 <= len(entries) <= 500

    entries.sort(key=lambda e: e.get("id", ""))
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text(report(entries, fails, warns, load_errors) + "\n",
                   encoding="utf-8")

    print(f"entries={len(entries)} fails={len(fails)+len(load_errors)} warns={len(warns)}")
    print(f"-> {OUT.relative_to(ROOT)}")
    print(f"-> {LOG.relative_to(ROOT)}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
