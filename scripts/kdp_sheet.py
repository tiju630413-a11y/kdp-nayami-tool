#!/usr/bin/env python3
"""KDP 登録シート生成（仕様 §5 工程7）。

templates/kdp_sheet.md の {{placeholder}} を book.json / plan.md /
promo/description.md / 実測値で埋めて output/NNN_kdp_sheet.md を出す。

使い方: python3 scripts/kdp_sheet.py <NNN>
キーワード7個は books/NNN_*/kdp_meta.json から読む（無ければ雛形を出す）。
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, load_settings, find_book, combined_manuscript, char_count

KDP_META_TEMPLATE = {
    "keywords": ["", "", "", "", "", "", ""],
    "categories": ["（カテゴリ1 例: 自己啓発 > 人間関係）", "（カテゴリ2）"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nnn")
    args = ap.parse_args()
    cfg = load_settings()
    book = find_book(args.nnn)
    nnn = book.name[:3]

    meta_path = book / "book.json"
    if not meta_path.exists():
        print("FAIL: book.json がない（build_epub.py を先に実行して雛形を作る）")
        return 1
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    kmeta_path = book / "kdp_meta.json"
    if not kmeta_path.exists():
        kmeta_path.write_text(json.dumps(KDP_META_TEMPLATE, ensure_ascii=False,
                                         indent=2) + "\n", encoding="utf-8")
        print(f"kdp_meta.json の雛形を作成: {kmeta_path.relative_to(ROOT)}")
        print("キーワード7個・カテゴリ2個を埋めて再実行してください"
              "（plan.md のキーワード仮説と promo を参照）。")
        return 1
    kmeta = json.loads(kmeta_path.read_text(encoding="utf-8"))
    if not all(kmeta["keywords"]) or len(kmeta["keywords"]) != 7:
        print("FAIL: kdp_meta.json の keywords は7個すべて埋める")
        return 1

    desc_path = book / "promo" / "description.md"
    description = (desc_path.read_text(encoding="utf-8").strip()
                   if desc_path.exists() else "（promo 工程が未完了。description.md なし）")

    # 実測値
    text, _ = combined_manuscript(book)
    epub = next((ROOT / "output").glob(f"{nnn}_*.epub"), None)
    epub_mb = f"{epub.stat().st_size / 1048576:.2f}" if epub else "未ビルド"
    used = json.loads((book / "assets_used.json").read_text(encoding="utf-8")) \
        if (book / "assets_used.json").exists() else {}
    conv = book / "reviews" / "converged.md"
    loops = ""
    if conv.exists():
        m = re.search(r"round(\d+)", conv.read_text(encoding="utf-8"))
        loops = m.group(1) if m else "?"

    values = {
        "title": meta.get("title", ""),
        "subtitle": meta.get("subtitle", ""),
        "series_name": meta.get("series_name", ""),
        "series_number": str(meta.get("series_number", "")),
        "description": description,
        "category_1": kmeta["categories"][0],
        "category_2": kmeta["categories"][1],
        "price_yen": str(cfg["price_yen"]),
        "epub_file": epub.name if epub else "未ビルド",
        "cover_file": "images/cover.jpg",
        "review_loops": loops or "未収束",
        "assets_used": str(len(used)),
        "min_author_assets": str(cfg["min_author_assets"]),
        "epub_size_mb": epub_mb,
        "pace_per_week": str(cfg["pace_per_week"]),
        "feedback_note": "（通読後に記入）",
    }
    for i, kw in enumerate(kmeta["keywords"], 1):
        values[f"keyword_{i}"] = kw

    tpl = (ROOT / "templates" / "kdp_sheet.md").read_text(encoding="utf-8")
    out_text = re.sub(r"\{\{(\w+)\}\}",
                      lambda m: values.get(m.group(1), f"{{{{{m.group(1)}}}}}"), tpl)
    out = ROOT / "output" / f"{nnn}_kdp_sheet.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(out_text, encoding="utf-8")
    print(f"生成: {out.relative_to(ROOT)}（字数 {char_count(text):,} / EPUB {epub_mb}MB）")
    unfilled = re.findall(r"\{\{(\w+)\}\}", out_text)
    if unfilled:
        print(f"WARN: 未充填プレースホルダ: {set(unfilled)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
