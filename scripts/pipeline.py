#!/usr/bin/env python3
"""工程オーケストレーション（仕様 §5）。

モデルAPIは呼ばない（D-10）。各工程の「次にやること」を指示書として出し、
成果物の存在と品質ゲートを機械検査して次工程を解放する。
モデルを差し替えても（Fable→Opus 4.8）、叩くコマンドは変わらない。

使い方:
  python3 scripts/pipeline.py status <NNN>          # 工程の進捗表示
  python3 scripts/pipeline.py next <NNN>            # 次工程の実行指示書を生成
  python3 scripts/pipeline.py new <slug>            # 新規企画のワークスペース作成
  python3 scripts/pipeline.py review <NNN> --round R           # 観点別レビュー指示書6枚を生成
  python3 scripts/pipeline.py review <NNN> --round R --collect # findings 集計・収束判定
  python3 scripts/pipeline.py gate <NNN>            # 品質ゲート §8 の機械検査
  python3 scripts/pipeline.py assets-sync <NNN>     # assets_used.json → used_in 反映
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (ROOT, load_settings, find_book, combined_manuscript,
                     char_count, load_assets, save_assets)

# 工程の順序と「完了」の判定材料
STAGES = [
    ("plan",        "plan.md",              "prompts/01_plan.md"),
    ("title",       "title.md",             "prompts/01b_title.md"),
    ("outline",     "outline.md",           "prompts/02_outline.md"),
    ("baseline",    "baseline.md",          "prompts/04_review_loop.md（ベースライン生成節）"),
    ("draft",       "draft/_draft_done",    "prompts/03_draft.md"),
    ("review_loop", "reviews/converged.md", "prompts/04_review_loop.md"),
    ("style_pass",  "_work/style_pass_log.md", "prompts/05_style.md"),
    ("images",      "images/image_spec.md", "prompts/06_images.md"),
    ("build",       None,                   "scripts/build_epub.py + scripts/kdp_sheet.py"),
    ("promo",       "promo/x_posts.md",     "prompts/08_promo.md"),
]

REVIEW_PERSPECTIVES = {
    "beginner": (
        "初心者読者",
        "この分野の予備知識がまったくない、疲れて集中力の落ちた夜の読者",
        ["style/guide.md"],
        "前提知識なしで再現できない手順がある / 専門用語が言い換えなしで使われる / 章の冒頭で迷子になる / 「はじめに」の約束と各章の手順が矛盾する",
    ),
    "harsh_reviewer": (
        "辛口Amazonレビュアー",
        "星1レビューを書く直前の、期待を裏切られた購入者。style/review_checklist.md の全項目を1つずつ適用する",
        ["style/review_checklist.md"],
        "review_checklist.md のいずれかの項目が FAIL（該当項目番号を必ず書く）",
    ),
    "editor": (
        "編集者",
        "構成に責任を持つベテラン編集者。重複・冗長・バランス・タイトル回収を見る",
        ["books の outline.md（タイトル回収対応表を含む）"],
        "同じ主張の章が2つある / 言い換えによる水増し節がある / タイトル回収対応表に穴がある / 章の実字数が計画から±30%超",
    ),
    "fact_checker": (
        "事実確認者",
        "医療・法律・金銭の記述に法的・倫理的責任を負う校閲者",
        ["style/guide.md の §3.3（専門家誘導定型文）"],
        "診断的表現がある / 医療・法律・金銭に触れる章に専門家誘導定型文がない / 出典のない統計・断定的な因果がある",
    ),
    "style_guard": (
        "文体番人",
        "著者「智珠」の声を守る担当。AIっぽさと guide.md 逸脱を見る",
        ["style/guide.md", "style/ng_phrases.txt"],
        "ng_phrases 該当が残っている / 声が章によって別人 / 章冒頭が一般論から始まる / 命令形の連発（説教調）",
    ),
    "ai_substitute": (
        "AI代替判定者",
        "「この本、無料のAIチャットで済むのでは?」を検証する読者代表。baseline.md（素のAI回答の実生成）と章ごとに比較する",
        ["books の baseline.md", "data/author_assets/assets.json（追加注入の候補出しに使う）"],
        "固有事例・断言・命名フレームワーク・実行装置の4面のうち、1面でも baseline を明確に上回れない章がある",
    ),
    "jp_quality": (
        "日本語品質番人",
        "日本語の質を三軸（漢字水準・誤用・自然さ）で校閲し、japanese_quality_prompt.md を唯一の基準に要修正箇所を洗い出す校閲者",
        ["japanese_quality_prompt.md（三軸の基準・唯一の参照元）"],
        "軸1（漢字水準：ジャンル上限を超える難読漢字を開いていない）・軸2（誤用：ら抜き/さ入れ/主述のねじれ/二重敬語/慣用句の誤用/重言/表記ゆれ等）・軸3（自然さ：同長文3連続・段落頭の接続詞連発・同一語尾4連続・AI常套句等）のいずれかで『要修正』にあたる箇所がある（該当軸を明記）",
    ),
}

# jp_quality 観点にだけ足す追加指示（三軸の判定行と、ジャンル別の漢字上限）
JP_QUALITY_EXTRA = """
## 三軸の判定（findings 表の前に必ず記載）
- 漢字水準: 合格 / 要修正
- 誤用: 合格 / 要修正
- 自然さ: 合格 / 要修正

各指摘は「該当箇所の引用・軸（漢字/誤用/自然さ）・問題・修正案」を含めること。
修正は原文の意図・雰囲気を壊さない範囲にとどめる（過剰な書き換えはしない）。
「要修正」が一つでもある箇所は重大指摘として SEVERE_COUNT に数える。
"""


def resolve_kanji_level(book):
    """book.json の genre（未指定＝実用書）から、この本の漢字上限を settings で解決する。"""
    cfg = load_settings()
    jq = cfg.get("japanese_quality", {}) if isinstance(cfg, dict) else {}
    default_level = jq.get("default_kanji_level", "準2級")
    novel_level = jq.get("novel_kanji_level", "2級")
    genre = "実用書"
    bj = book / "book.json"
    if bj.exists():
        try:
            genre = json.loads(bj.read_text(encoding="utf-8")).get("genre") or "実用書"
        except (ValueError, OSError):
            pass
    level = novel_level if genre == "小説" else default_level
    return genre, level


def stage_done(book, stage, artifact):
    if stage == "build":
        nnn = book.name[:3]
        return any((ROOT / "output").glob(f"{nnn}_*.epub"))
    return (book / artifact).exists()


def cmd_status(book):
    cfg = load_settings()
    print(f"=== {book.name} ===")
    nxt = None
    for stage, artifact, prompt in STAGES:
        done = stage_done(book, stage, artifact)
        mark = "✔" if done else ("→" if nxt is None else " ")
        if not done and nxt is None:
            nxt = (stage, prompt)
        print(f" {mark} {stage:12s} {'完了' if done else ''}")
    if (book / "draft").exists():
        text, drafts = combined_manuscript(book)
        print(f" 草稿: {len(drafts)}章 / {char_count(text):,}字（下限 {cfg['min_chars']:,}）")
    if nxt:
        print(f"\n次工程: {nxt[0]}（プロンプト: {nxt[1]}）")
        print(f"指示書生成: python3 scripts/pipeline.py next {book.name[:3]}")
    else:
        print("\n全工程完了。品質ゲート: python3 scripts/pipeline.py gate " + book.name[:3])


def cmd_new(slug):
    books = sorted((ROOT / "books").glob("[0-9][0-9][0-9]_*"))
    nnn = f"{int(books[-1].name[:3]) + 1:03d}" if books else "001"
    book = ROOT / "books" / f"{nnn}_{slug}"
    for d in ("draft", "reviews", "images", "promo", "_work"):
        (book / d).mkdir(parents=True)
    (book / "assets_used.json").write_text("{}\n", encoding="utf-8")
    print(f"作成: {book.relative_to(ROOT)}")
    print(f"次: python3 scripts/pipeline.py next {nnn}")


def cmd_next(book):
    for stage, artifact, prompt in STAGES:
        if not stage_done(book, stage, artifact):
            break
    else:
        print("全工程完了済み。gate を実行してください。")
        return
    nnn = book.name[:3]
    work = book / "_work"
    work.mkdir(exist_ok=True)
    lines = [
        f"# 実行指示書: {book.name} / 工程 {stage}",
        "",
        f"生成日: {date.today().isoformat()}（pipeline.py next により生成）",
        "",
        f"1. `{prompt}` を読み、指示に従って実行する",
        f"2. 完了物: `{book.relative_to(ROOT)}/{artifact or 'output/…epub'}`",
        f"3. 完了後: `python3 scripts/pipeline.py status {nnn}` で次工程を確認",
        "",
        "## この工程の注意",
    ]
    notes = {
        "plan": ["著者資産の残量を先に確認（不足なら prompts/00_asset_intake.md で補充が先）"],
        "baseline": ["**履歴なしの別コンテキスト**で素のプロンプトを実生成すること（このセッションで書かない）",
                      f"保存先: books/{book.name}/baseline.md（編集禁止）"],
        "draft": ["1〜2章ずつ。全章完了したら `touch books/" + book.name + "/draft/_draft_done`",
                   "章ごとに assets_used.json を更新"],
        "review_loop": [f"python3 scripts/pipeline.py review {nnn} --round 1 で観点別指示書を生成",
                         "6観点は**独立したコンテキスト**で実行（同一会話で連続実行しない）"],
        "build": [f"python3 scripts/build_epub.py {nnn} && python3 scripts/kdp_sheet.py {nnn}",
                   "book.json（タイトル・シリーズ・発行日）を先に作る（build_epub.py が雛形を出す）"],
    }
    lines += [f"- {n}" for n in notes.get(stage, ["特になし"])]
    out = work / "next_step.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"指示書: {out.relative_to(ROOT)}")
    print(f"工程: {stage} / プロンプト: {prompt}")


def cmd_review(book, rnd, collect):
    rdir = book / "reviews" / f"round{rnd}"
    nnn = book.name[:3]
    if collect:
        total, missing = 0, []
        for key in REVIEW_PERSPECTIVES:
            f = rdir / f"{key}_findings.md"
            if not f.exists():
                missing.append(key)
                continue
            m = re.search(r"SEVERE_COUNT:\s*(\d+)", f.read_text(encoding="utf-8"))
            n = int(m.group(1)) if m else -1
            if n < 0:
                missing.append(f"{key}（SEVERE_COUNT 行なし）")
            else:
                total += n
        if missing:
            print(f"未完了の観点: {', '.join(missing)}")
            return 1
        print(f"round{rnd} 重大指摘 合計: {total}")
        log = ROOT / "logs" / f"reviews_{nnn}.md"
        with log.open("a", encoding="utf-8") as fh:
            fh.write(f"- {date.today().isoformat()} round{rnd}: SEVERE合計 {total}\n")
        cfg = load_settings()
        if total == 0:
            (book / "reviews" / "converged.md").write_text(
                f"収束: round{rnd}（{date.today().isoformat()}）重大指摘ゼロ\n",
                encoding="utf-8")
            print("収束。次工程: style_pass")
        elif rnd >= cfg["max_review_loops"]:
            (book / "reviews" / "escalation.md").write_text(
                f"round{rnd} で未収束（重大指摘 {total}）。人間の判断が必要。\n"
                f"各観点の findings と revision_notes を確認してください。\n",
                encoding="utf-8")
            print(f"最大周回（{cfg['max_review_loops']}）到達・未収束 → エスカレーション")
        else:
            print(f"改稿後: python3 scripts/pipeline.py review {nnn} --round {rnd + 1}")
        return 0

    rdir.mkdir(parents=True, exist_ok=True)
    if not (book / "baseline.md").exists():
        print("FAIL: baseline.md がない。先にベースライン生成（prompts/04 参照）")
        return 1
    for key, (name, persona, refs, severe) in REVIEW_PERSPECTIVES.items():
        task = rdir / f"{key}_task.md"
        refs_lines = "\n".join(f"- {r}" for r in refs)
        extra = ""
        if key == "jp_quality":
            genre, level = resolve_kanji_level(book)
            extra = (f"\n## この本のジャンルと漢字上限\n"
                     f"- ジャンル: {genre} ／ 漢字上限: {level}"
                     f"（実用書＝準2級厳守／小説＝2級まで可。基準は japanese_quality_prompt.md 軸1）\n"
                     + JP_QUALITY_EXTRA)
        task.write_text(f"""# レビュー任務: {name}

あなたは{persona}です。以下の原稿を批評してください。
あなたの仕事は褒めることではなく、出版を止める欠陥を見つけることです。
指摘ゼロで返すのは、全文を検査し尽くした場合だけにしてください。
この任務は単独で完結します（他のレビュアーの結果を参照しない）。

## 読むもの
- 原稿: books/{book.name}/draft/ 以下の全 .md
- 判定基準:
{refs_lines}

## 重大指摘の基準（該当すれば「重大」）
{severe}
{extra}
## 出力形式
`books/{book.name}/reviews/round{rnd}/{key}_findings.md` に保存:

| # | 重大/軽微 | 章 | 該当箇所（引用10-30字） | 指摘 | 修正の方向 |
|---|---|---|---|---|---|

最終行に必ず: `SEVERE_COUNT: <重大指摘の数>`
""", encoding="utf-8")
    print(f"観点別指示書 {len(REVIEW_PERSPECTIVES)}枚: {rdir.relative_to(ROOT)}/*_task.md")
    print("各指示書を独立したコンテキストで実行後: "
          f"python3 scripts/pipeline.py review {nnn} --round {rnd} --collect")
    return 0


def cmd_assets_sync(book):
    used = json.loads((book / "assets_used.json").read_text(encoding="utf-8"))
    assets = load_assets()
    bid = book.name
    n = 0
    for a in assets:
        if a["id"] in used and bid not in a["used_in"]:
            a["used_in"].append(bid)
            n += 1
    save_assets(assets)
    print(f"used_in 反映: {n}件（{bid}）")


def cmd_gate(book):
    cfg = load_settings()
    nnn = book.name[:3]
    results = []  # (no, PASS/FAIL/MANUAL, desc)

    text, _ = combined_manuscript(book)
    total = char_count(text)
    results.append((1, "PASS" if total >= cfg["min_chars"] else "FAIL",
                    f"総字数 {total:,} / {cfg['min_chars']:,}"))

    conv = (book / "reviews" / "converged.md").exists()
    results.append((2, "PASS" if conv else "FAIL",
                    "review_loop 収束（converged.md）" + ("" if conv else " なし")))

    base = (book / "baseline.md").exists()
    results.append((3, "PASS" if base and conv else "FAIL",
                    "AI代替判定（baseline 存在＋収束に ai_substitute 含む）"))

    used = json.loads((book / "assets_used.json").read_text(encoding="utf-8"))
    results.append((4, "PASS" if len(used) >= cfg["min_author_assets"] else "FAIL",
                    f"著者資産 {len(used)} / {cfg['min_author_assets']}件"))

    import subprocess
    comb = book / "_work" / "manuscript_combined.md"
    comb.parent.mkdir(exist_ok=True)
    comb.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "style_check.py"),
                        str(comb)], capture_output=True, text=True)
    results.append((5, "PASS" if r.returncode == 0 else "FAIL",
                    "style_check " + ("PASS" if r.returncode == 0 else
                                       "FAIL（style_check を直接実行して確認）")))

    results.append((6, "MANUAL", "医療・法律・金銭の断定回避＋専門家誘導"
                    "（fact_checker findings で確認済みのこと）"))

    sheet = next((ROOT / "output").glob(f"{nnn}_*kdp_sheet.md"), None)
    ok7 = bool(sheet) and "あり" in sheet.read_text(encoding="utf-8")
    results.append((7, "PASS" if ok7 else "FAIL", "AI生成申告=あり（登録シート）"))

    # 奥付は build_epub が巻末（back.xhtml）に生成するため EPUB 内を検査する
    epub = next((ROOT / "output").glob(f"{nnn}_*.epub"), None)
    ok8 = False
    if epub:
        import zipfile
        with zipfile.ZipFile(epub) as z:
            if "OEBPS/back.xhtml" in z.namelist():
                back = z.read("OEBPS/back.xhtml").decode("utf-8")
                ok8 = "機械学習" in back and "©" in back and "初版発行" in back
    results.append((8, "PASS" if ok8 else "FAIL",
                    "奥付・著作権表記（EPUB巻末に © / 機械学習禁止文 / 発行日）"))

    if epub:
        mb = epub.stat().st_size / 1048576
        results.append((9, "PASS" if mb <= 3.5 else "FAIL",
                        f"EPUB {mb:.2f}MB（表紙の縮小視認テストは image_spec.md 手順で目視）"))
    else:
        results.append((9, "FAIL", "EPUB 未ビルド"))

    hr = book / "human_readthrough.md"
    results.append((10, "PASS" if hr.exists() else "MANUAL",
                    "人間の通読1回（human_readthrough.md に修正数と還流先を記録）"))

    # 11. 日本語三軸品質（jp_quality レビュー合格＝要修正ゼロ）。基準は japanese_quality_prompt.md
    rounds = sorted((book / "reviews").glob("round*"),
                    key=lambda p: int(re.sub(r"\D", "", p.name) or 0))
    jpf = next((r / "jp_quality_findings.md" for r in reversed(rounds)
                if (r / "jp_quality_findings.md").exists()), None)
    genre, level = resolve_kanji_level(book)
    if jpf is None:
        results.append((11, "MANUAL", f"日本語三軸品質（jp_quality 未実施／漢字上限 {level}）"
                        "。review_loop で jp_quality を回す"))
    else:
        m = re.search(r"SEVERE_COUNT:\s*(\d+)", jpf.read_text(encoding="utf-8"))
        nsev = int(m.group(1)) if m else -1
        results.append((11, "PASS" if nsev == 0 else "FAIL",
                        f"日本語三軸品質（漢字水準・誤用・自然さ）要修正 {max(nsev,0)}件"
                        f"／漢字上限 {level}（{genre}）"))

    print(f"=== 品質ゲート: {book.name} ===")
    fails = 0
    for no, verdict, desc in results:
        print(f" {no:2d}. [{verdict}] {desc}")
        fails += verdict == "FAIL"
    print("\n判定: " + ("出版可（MANUAL項目は人間が確認）" if fails == 0
                        else f"出版不可（FAIL {fails}件）"))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["status", "next", "new", "review",
                                         "gate", "assets-sync"])
    ap.add_argument("target", help="書籍番号 NNN（new のときは slug）")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--collect", action="store_true")
    args = ap.parse_args()

    if args.command == "new":
        return cmd_new(args.target)
    book = find_book(args.target)
    if args.command == "status":
        return cmd_status(book)
    if args.command == "next":
        return cmd_next(book)
    if args.command == "review":
        return cmd_review(book, args.round, args.collect)
    if args.command == "gate":
        return cmd_gate(book)
    if args.command == "assets-sync":
        return cmd_assets_sync(book)


if __name__ == "__main__":
    sys.exit(main() or 0)
