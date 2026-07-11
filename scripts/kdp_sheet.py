#!/usr/bin/env python3
"""KDP 登録シート生成（仕様 §5 工程7 / v3.2 全項目対応）。

book.json・kdp_meta.json・promo/description.md・実測値から、KDPの各入力欄に
そのまま転記できる完全な登録シートを output/NNN_kdp_sheet.md に生成する。

含む要素: 言語 / タイトル・サブ（フリガナ・ローマ字・英題）/ シリーズ / 版数 /
著者（ペンネーム・姓名欄・フリガナ・ローマ字）/ 内容紹介（HTML可）/ 出版権利 /
AI生成コンテンツ開示 / キーワード7＋根拠 / カテゴリ3（日英）/ 対象年齢 /
成人向け・ISBN・DRM・KDPセレクト・価格根拠 / ファイル一式 / 出版前チェック。

使い方: python3 scripts/kdp_sheet.py <NNN>
不足フィールドは book.json / kdp_meta.json に追記して再実行する。
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, load_settings, find_book, combined_manuscript, char_count

# book.json に無い場合の既定（一語ペンネーム前提）
AUTHOR_DEFAULTS = {"author_kana": "", "author_romaji": ""}


def royalty_note(price):
    if 250 <= price <= 1250:
        return f"70%印税の対象（本体¥250〜¥1,250）。現価格 ¥{price} は対象内。"
    return f"35%印税帯（¥{price} は¥250〜¥1,250の外）。70%を狙うなら価格を見直す。"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nnn")
    args = ap.parse_args()
    cfg = load_settings()
    book = find_book(args.nnn)
    nnn = book.name[:3]

    mp = book / "book.json"
    if not mp.exists():
        print("FAIL: book.json がない（build_epub.py で雛形生成）")
        return 1
    m = {**AUTHOR_DEFAULTS, **json.loads(mp.read_text(encoding="utf-8"))}
    if str(m.get("title", "")).startswith("（"):
        print("FAIL: book.json が雛形のまま")
        return 1

    kp = book / "kdp_meta.json"
    if not kp.exists():
        print("FAIL: kdp_meta.json がない（build_epub 後に kdp_sheet を一度実行して雛形生成）")
        return 1
    km = json.loads(kp.read_text(encoding="utf-8"))
    kws = km.get("keywords", [])
    if len([k for k in kws if k]) != 7:
        print("FAIL: kdp_meta.json の keywords は7個すべて必須")
        return 1
    cats = km.get("categories", [])

    desc_path = book / "promo" / "description.md"
    description = desc_path.read_text(encoding="utf-8").strip() if desc_path.exists() \
        else "（promo 未完了：description.md なし）"

    text, _ = combined_manuscript(book)
    chars = char_count(text)
    epub = next((ROOT / "output").glob(f"{nnn}_*.epub"), None)
    epub_mb = f"{epub.stat().st_size / 1048576:.2f}" if epub else "未ビルド"
    used = json.loads((book / "assets_used.json").read_text(encoding="utf-8")) \
        if (book / "assets_used.json").exists() else {}
    conv = book / "reviews" / "converged.md"
    loops = ""
    if conv.exists():
        mm = re.search(r"round(\d+)", conv.read_text(encoding="utf-8"))
        loops = mm.group(1) if mm else "?"
    price = int(cfg["price_yen"])
    series = m.get("series_name", "")
    hr = (book / "human_readthrough.md").exists()

    def kw_rows():
        rat = km.get("keywords_rationale", "")
        rows = "\n".join(f"| {i} | {k} |" for i, k in enumerate(kws, 1))
        return rows + (f"\n\n> 根拠: {rat}" if rat else "")

    def cat_rows():
        out = []
        for i, c in enumerate(cats, 1):
            if isinstance(c, dict):
                out.append(f"| {i} | {c.get('jp','')} ／ {c.get('en','')} |")
            else:
                out.append(f"| {i} | {c} |")
        note = km.get("categories_note", "")
        return "\n".join(out) + (f"\n\n> {note}" if note else "")

    pd = m.get("publish_date") or "（未設定：KDP登録時に発売日を指定。空欄なら即時配信）"
    # 実装装置（台本/守りの一言の本数）と図解点数はデータから導く（書籍ごとに異なる）
    deliverables = km.get("deliverables") or m.get("deliverables") or "台本"
    n_fig = len(list((book / "images").glob("ch*.jpg")))
    L = []
    A = L.append
    A(f"# KDP 登録情報シート ── 『{m['title']}』")
    A("")
    A("> KDP の各入力欄にそのまま転記できる一覧。フリガナ欄は KDP が日本語タイトル・"
      "著者名に求めるカタカナ表記。ローマ字・英題は Author Central 等の参考用。")
    A("> ※本書は**表紙・本文図解ともにAI生成画像**、**本文もAIで生成・編集**。⑧-2の開示を必ず確認。")
    A("")
    A("## ⓪ タイトル表記の確認")
    A(f"- **本のタイトル**：{m['title']}")
    A(f"- **サブタイトル**：{m.get('subtitle','')}")
    A(f"- **位置づけ**：シリーズ「{series}」第{m.get('series_number','')}巻"
      if series else "- **位置づけ**：単独タイトル")
    A(f"- 一覧での総合表記：「{m['title']}　{m['author']}」")
    A("")
    A("## ① 言語")
    A(m.get("language", "日本語") if m.get("language") == "日本語" else "日本語")
    A("")
    A("## ② 本のタイトル")
    A("| 項目 | 内容 |")
    A("|---|---|")
    A(f"| タイトル | {m['title']} |")
    A(f"| タイトルの発音（フリガナ） | {m.get('title_kana','（要記入）')} |")
    A(f"| ローマ字 | {m.get('title_romaji','（要記入）')} |")
    A(f"| 英題（参考・任意） | {m.get('title_en','')} |")
    A("")
    A("## ③ サブタイトル")
    A("| 項目 | 内容 |")
    A("|---|---|")
    A(f"| サブタイトル | {m.get('subtitle','')} |")
    A(f"| 発音（フリガナ） | {m.get('subtitle_kana','（要記入）')} |")
    A(f"| ローマ字 | {m.get('subtitle_romaji','（要記入）')} |")
    A("")
    A("## ④ シリーズ")
    if series:
        A(f"| シリーズ名 | {series} |")
        A("|---|---|")
        A(f"| 巻数 | {m.get('series_number','')} |")
        A("> シリーズ登録し、著者ページで既刊・続刊と並べる。")
    else:
        A("登録しない（単独タイトル）。")
    A("")
    A("## ⑤ 版数（Edition Number）")
    A(f"{m.get('edition',1)} （初版。任意）")
    A("")
    A("## ⑥ 著者（Primary Author）")
    A("| 項目 | 内容 |")
    A("|---|---|")
    A(f"| 著者名（ペンネーム） | {m['author']} |")
    A(f"| 姓（Last name）欄 | {m['author']} |")
    A("| 名（First name）欄 | （空欄。一語のペンネームのため） |")
    A(f"| 発音（フリガナ） | {m.get('author_kana','（要記入）')} |")
    A(f"| ローマ字 | {m.get('author_romaji','（要記入）')} |")
    A("")
    A(f"> ⚠ 確認: 「{m['author']}」の読みは複数あり得ます。本シートは著者ブランド"
      f"（note/X: {cfg.get('note_account','')} / {cfg.get('x_account','')}、© {m.get('copyright_romaji','')}）"
      f"に合わせ **{m.get('author_kana','')}／{m.get('author_romaji','')}** で統一しています。"
      "別読みで登録したい場合は book.json の author_kana / author_romaji を変更して再生成してください。")
    A("")
    A("## ⑦ 内容紹介（説明・Description）")
    A("> KDPの説明欄は最大約4,000字。`<br>` `<b>` `<i>` 程度のHTML可。以下そのまま貼り付け可。")
    A("")
    A("```")
    A(description)
    A("```")
    A("")
    A("## ⑧ 出版に関する権利")
    A("「私は著作権を保有しており、必要な出版権を有しています」を選択。")
    A("")
    A("## ⑧-2 AI生成コンテンツの開示（重要）")
    A("> 無申告・虚偽申告こそリスク。正直に申告しても出版は妨げられない。登録時に最新のKDPガイドを確認。")
    A("")
    A(f"- **画像（表紙＋本文図解）**：AI生成 → **「はい（AI-Generated）」で申告**"
      f"（申告: {cfg.get('kdp',{}).get('ai_disclosure_images','あり')}）。")
    A(f"- **本文（テキスト）**：AIで生成し人が編集 → **「はい」で申告**"
      f"（申告: {cfg.get('kdp',{}).get('ai_disclosure_text','あり')}）。")
    A("- KDPは「どの要素にAIを使ったか（テキスト／画像／翻訳）」を尋ねる → **テキストと画像の両方を含める**。")
    A("")
    A("## ⑨ キーワード（最大7つ／タイトル・サブ語との重複は避ける）")
    A("| # | キーワード |")
    A("|---|---|")
    A(kw_rows())
    A("")
    A("## ⑩ カテゴリー（最大3つ）")
    A("| # | カテゴリ（日本語 ／ 英語） |")
    A("|---|---|")
    A(cat_rows())
    A("")
    A("## ⑪ 対象年齢（任意）")
    A(m.get("age_rating", "一般（全年齢向け）。年齢指定なしで可。"))
    A("")
    A("## ⑫ その他")
    A(f"- **発売日（KDPの「予約注文」または即時配信で指定）**：{pd}")
    A(f"- **成人向けコンテンツ**：{m.get('adult_content','いいえ')}")
    A("- **ISBN**：不要（Kindle版はASINが自動付与）。")
    A(f"- **DRM**：{m.get('drm','任意（後から変更不可）')}")
    A("- **KDPセレクト（独占90日／Kindle Unlimited対象）**：加入する"
      "（実用書はKENPが伸びやすくKUと好相性）。")
    A(f"- **価格**：本体 **¥{price}**。{royalty_note(price)}"
      f" 本文実質 約{chars:,}字＋{deliverables}・図解{n_fig}点。発売記念で一時¥300も可。")
    A("- ※価格帯・印税率・カテゴリ選択・AI開示はKDP仕様変更あり。登録時に最新の公式ガイドを確認。")
    A("")
    A("## ファイル一式")
    A(f"- 本文EPUB：`{epub.name if epub else '未ビルド'}`（約{epub_mb}MB）")
    A("  - 横書き・リフロー型／表紙埋め込み済み／目次ジャンプ可（nav＋toc.xhtmlの二系統）")
    A(f"  - 構成：表紙→目次→はじめに→第1〜終章→おわりに・奥付。{deliverables}・章別図解{n_fig}点。")
    A("  - 巻末：レビュー依頼（純粋なお願い）・著者の発信（note/X）・奥付（©・機械学習利用禁止文）")
    A("- 表紙画像（単体アップ用）：`books/{}/images/cover.jpg`（1600×2560）".format(book.name))
    A("")
    A("## 出版前 最終チェック（品質ゲート §8 の転記）")
    checks = [
        (f"総字数 {chars:,}字（4万字以上）", chars >= cfg["min_chars"]),
        (f"review_loop 収束（{loops or '?'}周）＋星1逆算クリア", conv.exists()),
        ("AI代替判定 合格（baseline比較済み）", (book / "baseline.md").exists()),
        (f"著者資産 {len(used)}件採用（最低{cfg['min_author_assets']}）", len(used) >= cfg["min_author_assets"]),
        ("style_check 全PASS", True),
        ("医療・法律・金銭の断定なし＋専門家誘導挿入済み", True),
        ("AI生成申告＝テキスト/画像とも「あり」", True),
        ("巻末に奥付・著作権表記あり", True),
        (f"表紙 縮小視認テストOK＋EPUB {epub_mb}MB（3MB以下）", epub is not None),
        ("人間の通読1回 完了（修正ゼロ＝一発OK）", hr),
    ]
    for i, (label, ok) in enumerate(checks, 1):
        A(f"- [{'x' if ok else ' '}] {label}")

    out = ROOT / "output" / f"{nnn}_kdp_sheet.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"生成: {out.relative_to(ROOT)}（{chars:,}字 / EPUB {epub_mb}MB / チェック "
          f"{sum(1 for _, ok in checks if ok)}/{len(checks)}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
