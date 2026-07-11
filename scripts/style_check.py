#!/usr/bin/env python3
"""文体チェッカー（仕様 §4.4）。

計測項目:
  1. 総字数（min_chars 未満は FAIL）
  2. 読点密度（読点間隔の分布。閾値は config/settings.yaml）
  3. 文末重複率（同一文末の連続 > max_same_ending_run で指摘）
  4. NG表現検出（style/ng_phrases.txt）
  5. 段落長分布（max_paragraph_chars 超で WARN）
  6. 具体性密度（「たとえば」「ケース」「場面」等の章あたり出現数）
  7. 診断的表現の検出（医療・法律・金銭の断定）
  8. 簡易誤字パス（重複助詞・重ね言葉）
  9. AI的な二重引用符（" " " 等）の検出（日本語は「」『』）
  10. 感嘆符・疑問符の乱発（1000字あたり／連続）
  11. 1文の読点過多（句読点の過剰使用）

使い方:
  python3 scripts/style_check.py <原稿.md> [--json] [--min-chars N]
原稿は Markdown。見出し行（#）・コードブロックは本文統計から除外。
「## 」を章の区切りとして具体性密度を章別に測る。
出力: PASS/FAIL ＋ 修正箇所リスト。終了コード 0=PASS / 1=FAIL。
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULTS = {
    "min_chars": 40000,
    "kuten_interval_min": 7,
    "kuten_interval_max": 14,
    "max_same_ending_run": 2,
    "max_paragraph_chars": 400,
    "min_concrete_per_chapter": 3,
    "max_kuten_per_sentence": 5,   # 1文の読点上限（超で WARN。句読点の過剰使用検出）
    "max_exclaim_per_1000": 3,     # ！／？ の1000字あたり上限（超で WARN。乱発検出）
}

# AIがよく使う二重引用符（日本語本文では「」『』を使う）。半角"・全角“”・〝〟
AI_QUOTE_CHARS = ['"', "“", "”", "〝", "〟"]

CONCRETE_MARKERS = ["たとえば", "例えば", "ケース", "場面", "ある日", "あるとき",
                    "実際に", "具体的に", "台本", "ワーク"]

# 診断的・断定的表現（医療・法律・金銭）
DIAGNOSTIC_PATTERNS = [
    (r"あなたは[^。]{0,15}(障害|病|うつ|依存症)[^。]{0,6}(かも|です|でしょう)", "診断的表現（医療）"),
    (r"(それ|これ)は[^。]{0,10}(病気|うつ病|障害)です", "診断的表現（医療）"),
    (r"(必ず|絶対に?)[^。]{0,12}(治り|治し|勝て|儲か|得し)", "断定（医療・法律・金銭）"),
    (r"(訴え|裁判)[^。]{0,8}(れば|たら)[^。]{0,10}勝て", "断定（法律）"),
    (r"(元本保証|確実に増え|損しない投資)", "断定（金銭）"),
]

# 簡易誤字: 重複助詞・重ね言葉
TYPO_PATTERNS = [
    (r"(?<![ぁ-ん])([をにへがはで])\1", "助詞の重複"),
    (r"(things|ということ)がが", "助詞の重複"),
    (r"頭痛が痛", "重ね言葉"),
    (r"一番最初|一番最後", "重ね言葉"),
    (r"まず最初に", "重ね言葉"),
    (r"あとで後悔", "重ね言葉"),
    (r"([ぁ-んァ-ヶ一-龠])\1\1\1", "同一文字4連続（入力ミス疑い）"),
]


def load_settings():
    """config/settings.yaml から style_check 閾値を読む（PyYAML 非依存の簡易パーサ）。"""
    cfg = dict(DEFAULTS)
    path = ROOT / "config" / "settings.yaml"
    if not path.exists():
        return cfg
    in_block = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^style_check:\s*$", line):
            in_block = True
            continue
        if in_block:
            m = re.match(r"^\s{2}(\w+):\s*(\d+)", line)
            if m and m.group(1) in cfg:
                cfg[m.group(1)] = int(m.group(2))
            elif line and not line.startswith(" "):
                in_block = False
        m = re.match(r"^min_chars:\s*(\d+)", line)
        if m:
            cfg["min_chars"] = int(m.group(1))
    return cfg


def load_ng_phrases():
    path = ROOT / "style" / "ng_phrases.txt"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def strip_markup(text):
    """コードブロック・見出し記号を除いた本文を返す。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    lines = []
    for ln in text.splitlines():
        if ln.startswith("#"):
            continue
        lines.append(ln)
    return "\n".join(lines)


def split_sentences(text):
    body = re.sub(r"\s", "", strip_markup(text))
    return [s for s in re.split(r"(?<=[。！？!?])", body) if s]


def check(path, cfg):
    raw = Path(path).read_text(encoding="utf-8")
    body = strip_markup(raw)
    body_flat = re.sub(r"\s", "", body)
    issues = []   # (severity, message) severity: FAIL/WARN
    stats = {}

    # 1. 総字数
    total = len(body_flat)
    stats["total_chars"] = total
    if total < cfg["min_chars"]:
        issues.append(("FAIL", f"総字数 {total:,} 字 < 下限 {cfg['min_chars']:,} 字"))

    # 2. 読点密度
    intervals = []
    for seg in re.split(r"[。！？!?\n]", body_flat):
        parts = seg.split("、")
        for p in parts[:-1]:
            intervals.append(len(p))
    if intervals:
        avg = sum(intervals) / len(intervals)
        stats["kuten_interval_avg"] = round(avg, 1)
        if avg < cfg["kuten_interval_min"]:
            issues.append(("WARN", f"読点間隔 平均{avg:.1f}字（細切れ。目安9〜11）"))
        elif avg > cfg["kuten_interval_max"]:
            issues.append(("WARN", f"読点間隔 平均{avg:.1f}字（息が長い。目安9〜11）"))

    # 3. 文末重複
    sents = split_sentences(raw)
    endings = []
    for s in sents:
        m = re.search(r"([ぁ-ん一-龠ァ-ヶ]{1,3})[。！？!?]$", s)
        endings.append(m.group(1)[-2:] if m else "")
    run, prev, run_starts = 1, None, []
    for i, e in enumerate(endings):
        if e and e == prev:
            run += 1
            if run == cfg["max_same_ending_run"] + 1:
                run_starts.append((i, e))
        else:
            run = 1
        prev = e
    stats["same_ending_violations"] = len(run_starts)
    for i, e in run_starts[:20]:
        ctx = sents[i][:30]
        issues.append(("FAIL", f"文末「{e}」が{cfg['max_same_ending_run']+1}連続: …{ctx}…"))

    # 4. NG表現
    ng_hits = []
    for ng in load_ng_phrases():
        cnt = body.count(ng)
        if cnt:
            ng_hits.append((ng, cnt))
    stats["ng_phrase_hits"] = sum(c for _, c in ng_hits)
    for ng, cnt in ng_hits:
        issues.append(("FAIL", f"NG表現「{ng}」x{cnt}"))

    # 5. 段落長
    paras = [re.sub(r"\s", "", p) for p in re.split(r"\n\s*\n", body) if p.strip()]
    longs = [p for p in paras if len(p) > cfg["max_paragraph_chars"]]
    stats["long_paragraphs"] = len(longs)
    for p in longs[:10]:
        issues.append(("WARN", f"段落 {len(p)}字 > {cfg['max_paragraph_chars']}字: {p[:25]}…"))

    # 6. 具体性密度（章＝「## 」区切り）
    chapters = re.split(r"\n## ", raw)
    weak = []
    for ch in chapters:
        title = ch.splitlines()[0][:20] if ch.strip() else "?"
        cnt = sum(strip_markup(ch).count(m) for m in CONCRETE_MARKERS)
        if len(re.sub(r"\s", "", strip_markup(ch))) > 1500 and cnt < cfg["min_concrete_per_chapter"]:
            weak.append((title, cnt))
    stats["weak_concrete_chapters"] = len(weak)
    for t, c in weak:
        issues.append(("FAIL", f"章「{t}」の具体性マーカー {c} 個 < {cfg['min_concrete_per_chapter']}（具体例・台本・ワークを追加）"))

    # 7. 診断的表現
    for pat, label in DIAGNOSTIC_PATTERNS:
        for m in re.finditer(pat, body_flat):
            issues.append(("FAIL", f"{label}: …{m.group(0)}…"))

    # 8. 簡易誤字
    for pat, label in TYPO_PATTERNS:
        for m in re.finditer(pat, body):
            issues.append(("WARN", f"{label}: …{m.group(0)}…"))

    # 9. AI的な二重引用符（日本語本文は「」『』）。WARN で全数を挙げ style_pass で解消
    quote_hits = sum(body.count(q) for q in AI_QUOTE_CHARS)
    stats["ai_quote_hits"] = quote_hits
    if quote_hits:
        found = "".join(q for q in AI_QUOTE_CHARS if q in body)
        issues.append(("WARN", f"AI的な二重引用符 {quote_hits}箇所（{found}）"
                               "。会話・引用は「」、書名は『』、強調は最小限に置き換える"))

    # 10. 感嘆符・疑問符の乱発
    exclaim = len(re.findall(r"[！!？?]", body_flat))
    stats["exclaim_marks"] = exclaim
    if total >= 200:
        per1000 = exclaim * 1000 / max(total, 1)
        if per1000 > cfg["max_exclaim_per_1000"]:
            issues.append(("WARN", f"感嘆符・疑問符 {exclaim}個（1000字あたり{per1000:.1f}"
                                   f"／目安{cfg['max_exclaim_per_1000']}）。乱発を抑える"))
    for m in re.finditer(r"[！!？?]{2,}", body_flat):
        issues.append(("WARN", f"感嘆符・疑問符の連続「{m.group(0)}」。1つにする"))

    # 11. 1文の読点過多（句読点の過剰使用）。表・箇条書きは散文でないため除外
    over = []
    for ln in strip_markup(raw).splitlines():
        s0 = ln.strip()
        if not s0 or s0.startswith("|") or set(s0) <= set("|-: 　"):
            continue                                   # 表の行は除外
        s0 = re.sub(r"^([-*・]|\d+[.\)、]|[①-⑳])\s*", "", s0)  # 箇条書き先頭記号を除去
        for sent in re.split(r"(?<=[。！？!?])", s0):
            n = sent.count("、")
            if n > cfg["max_kuten_per_sentence"]:
                over.append((n, sent.strip()[:30]))
    stats["over_comma_sentences"] = len(over)
    for n, ctx in over[:10]:
        issues.append(("WARN", f"1文に読点{n}個（>{cfg['max_kuten_per_sentence']}）"
                               f"。文を割る: …{ctx}…"))

    fails = [m for s, m in issues if s == "FAIL"]
    warns = [m for s, m in issues if s == "WARN"]
    return stats, fails, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manuscript")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-chars", type=int, help="字数下限の上書き（章単位チェック用）")
    args = ap.parse_args()

    cfg = load_settings()
    if args.min_chars is not None:
        cfg["min_chars"] = args.min_chars

    stats, fails, warns = check(args.manuscript, cfg)
    verdict = "PASS" if not fails else "FAIL"

    if args.json:
        print(json.dumps({"verdict": verdict, "stats": stats,
                          "fails": fails, "warns": warns}, ensure_ascii=False, indent=2))
    else:
        print(f"=== style_check: {verdict} ===")
        print(f"総字数: {stats.get('total_chars', 0):,} / 読点間隔平均: {stats.get('kuten_interval_avg', '-')}")
        if fails:
            print(f"\n[FAIL] {len(fails)}件（全て修正するまで出版工程に進めない）")
            for m in fails:
                print(f"  - {m}")
        if warns:
            print(f"\n[WARN] {len(warns)}件")
            for m in warns:
                print(f"  - {m}")
        if not fails and not warns:
            print("指摘なし。")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
