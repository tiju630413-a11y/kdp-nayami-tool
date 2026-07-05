#!/usr/bin/env python3
"""EPUB ビルド（画像対応・圧縮込み。仕様 §5 工程7 / §4.5）。

- 入力: books/NNN_*/draft/ch*.md（章番号順）、books/NNN_*/images/、book.json
- 巻末: templates/back_matter.md の順序に従い、おわりに（ch99）→
  レビュー依頼（定型）→ 次の1冊 → note導線 → 奥付 を自動結合
- 画像: Pillow があれば設定値（config/settings.yaml: epub）で縮小・再圧縮。
  なければ WARN を出して原本サイズで格納（D-04）
- 出力: output/NNN_タイトル.epub。合計サイズ 3MB 超で WARN、3.5MB 超で FAIL

使い方:
  python3 scripts/build_epub.py <NNN> [--no-cover]
book.json が無い場合は雛形を書き出して終了する（値を埋めて再実行）。
"""
import argparse
import html
import json
import re
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, load_settings, find_book

BOOK_JSON_TEMPLATE = {
    "title": "（タイトル）",
    "subtitle": "（サブタイトル）",
    "series_name": "（シリーズ名）",
    "series_number": 1,
    "author": "智珠",
    "publish_date": "",  # 空なら今日
    "next_book_title": "",  # 1冊目は空でよい
    "next_book_pain_line": "",
    "note_url": "https://note.com/marvelous1101",
    "language": "ja",
}

CSS = """body { font-family: serif; line-height: 1.9; margin: 0 5%; }
h1 { font-size: 1.5em; margin: 2em 0 1.5em; line-height: 1.4; }
h2 { font-size: 1.3em; margin: 2em 0 1em; line-height: 1.4; }
h3 { font-size: 1.1em; margin: 1.5em 0 0.8em; }
p { margin: 0 0 1em; text-indent: 1em; }
p.noindent { text-indent: 0; }
blockquote { margin: 1em 1.5em; padding-left: 0.8em; border-left: 2px solid #999; }
ul, ol { margin: 1em 0; padding-left: 2em; }
img { max-width: 100%; }
.colophon { margin-top: 4em; font-size: 0.9em; }
.colophon p { text-indent: 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 2em 0; }
"""


def md_to_xhtml(md_text, chapter_title=None):
    """最小Markdown→XHTML変換（見出し/段落/強調/箇条書き/引用/画像/罫線）。"""
    out, in_list, in_quote = [], None, False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

    def close_quote():
        nonlocal in_quote
        if in_quote:
            out.append("</blockquote>")
            in_quote = False

    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        return s

    for line in md_text.splitlines():
        line = line.rstrip()
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            close_list(); close_quote()
            lvl = min(len(m.group(1)), 3)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line.strip())
        if m:
            close_list(); close_quote()
            name = Path(m.group(2)).name
            out.append(f'<p class="noindent"><img src="images/{name}" alt="{html.escape(m.group(1))}"/></p>')
            continue
        if re.match(r"^(---|\*\*\*)$", line.strip()):
            close_list(); close_quote()
            out.append("<hr/>")
            continue
        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            close_quote()
            if in_list != "ul":
                close_list(); out.append("<ul>"); in_list = "ul"
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue
        m = re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            close_quote()
            if in_list != "ol":
                close_list(); out.append("<ol>"); in_list = "ol"
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue
        m = re.match(r"^>\s?(.*)$", line)
        if m:
            close_list()
            if not in_quote:
                out.append("<blockquote>"); in_quote = True
            if m.group(1):
                out.append(f"<p>{inline(m.group(1))}</p>")
            continue
        if not line.strip():
            close_list(); close_quote()
            continue
        close_list(); close_quote()
        out.append(f"<p>{inline(line)}</p>")
    close_list(); close_quote()
    return "\n".join(out)


def xhtml_doc(title, body, lang="ja"):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{lang}" lang="{lang}">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title>
<link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{body}
</body></html>
"""


def back_matter_xhtml(meta, owarini_md):
    """templates/back_matter.md の順序で巻末を組む。"""
    pd = meta.get("publish_date") or date.today().isoformat()
    year = pd[:4]
    parts = []
    if owarini_md:
        parts.append(md_to_xhtml(owarini_md))
    parts.append("<hr/>")
    parts.append(md_to_xhtml(
        "## 読み終えたあなたへ\n\n"
        "最後まで読んでくださって、ありがとうございました。\n\n"
        "もしこの本のどこか一箇所でも、あなたの役に立った場面があったなら、"
        "レビューで教えていただけるとうれしいです。"
        "「第◯章の△△を試してみた」のような一言だけでも、"
        "次の本を書くうえで、何よりの道しるべになります。\n\n"
        "厳しい感想も、そのまま受け取ります。\n"))
    if meta.get("next_book_title"):
        parts.append(md_to_xhtml(
            "## 次に読む1冊\n\n"
            f"本書とあわせて読んでいただきたいのが、こちらです。\n\n"
            f"**『{meta['next_book_title']}』**（{meta['author']}）\n\n"
            f"{meta.get('next_book_pain_line','')}——そんなあなたに向けて書きました。\n"))
    elif meta.get("series_name"):  # 1冊目: 既刊がない間はシリーズ予告1行（templates/back_matter.md）
        parts.append(md_to_xhtml(
            f"今後も「{meta['series_name']}」シリーズとして、"
            "夜にひとりで抱えてしまう悩みに向けた一冊を、順に出していきます。\n"))
    if meta.get("note_url"):  # アカウント未確定の間は導線を省略（仕様§12）
        parts.append(md_to_xhtml(
            "## note のご案内\n\n"
            "本に書ききれなかった話や、日々の観察は note に書いています。\n\n"
            f"「{meta['author']}」で検索するか、こちらへ: {meta['note_url']}\n"))
    parts.append(f"""<div class="colophon"><hr/>
<p><strong>{html.escape(meta['title'])}</strong><br/>{html.escape(meta.get('subtitle',''))}</p>
<p>{html.escape(pd)}　初版発行</p>
<p>著者　{html.escape(meta['author'])}<br/>© {year} Chiju</p>
<p>本書の内容の一部または全部を、著作権者の許可なく複製・転載・翻案・データ化および機械学習の目的で利用することを禁じます。</p>
<p>本書は情報の提供を目的としたものであり、医療・法律・金銭に関する個別の助言に代わるものではありません。具体的な判断にあたっては、専門家にご相談ください。</p>
</div>""")
    return "\n".join(parts)


def compress_image(src, dst, max_width, quality):
    """Pillow があれば縮小・再圧縮。なければコピー（WARN）。戻り値: 説明文字列。"""
    try:
        from PIL import Image
    except ImportError:
        shutil.copy2(src, dst)
        return f"WARN: Pillow なし・無圧縮コピー {src.name}（pip install pillow で圧縮有効化）"
    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    if img.width > max_width:
        img = img.resize((max_width, round(img.height * max_width / img.width)),
                         Image.LANCZOS)
    img.save(dst, "JPEG", quality=quality, optimize=True)
    return f"{src.name}: {src.stat().st_size//1024}KB → {dst.stat().st_size//1024}KB"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nnn")
    ap.add_argument("--no-cover", action="store_true",
                    help="表紙なしでビルド（動作確認用。出版ゲートは通らない）")
    args = ap.parse_args()

    cfg = load_settings()
    ecfg = cfg.get("epub", {})
    max_w = int(ecfg.get("image_max_width", 1200))
    cover_w = int(ecfg.get("cover_max_width", 1600))
    quality = int(ecfg.get("image_quality", 80))
    max_mb = float(ecfg.get("max_total_mb", 3))

    book = find_book(args.nnn)
    meta_path = book / "book.json"
    if not meta_path.exists():
        meta_path.write_text(json.dumps(BOOK_JSON_TEMPLATE, ensure_ascii=False,
                                        indent=2) + "\n", encoding="utf-8")
        print(f"book.json の雛形を作成: {meta_path.relative_to(ROOT)}")
        print("タイトル等を埋めて再実行してください。")
        return 1
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta.get("title", "").startswith("（"):
        print("FAIL: book.json が雛形のまま（title を設定してください）")
        return 1

    drafts = sorted((book / "draft").glob("ch*.md"))
    drafts = [d for d in drafts if not d.name.startswith("ch99")]
    if not drafts:
        print("FAIL: draft/ch*.md がない")
        return 1
    owarini = book / "draft" / "ch99_owarini.md"
    owarini_md = owarini.read_text(encoding="utf-8") if owarini.exists() else None
    if not owarini_md:
        print("WARN: ch99_owarini.md がない（おわりに抜きでビルド）")

    # 画像収集・圧縮
    tmp_img = book / "_work" / "epub_images"
    tmp_img.mkdir(parents=True, exist_ok=True)
    for old in tmp_img.glob("*"):
        old.unlink()
    img_dir = book / "images"
    images, notes = [], []
    cover = None
    if img_dir.exists():
        for src in sorted(img_dir.iterdir()):
            if src.suffix.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            dst = tmp_img / (src.stem + ".jpg")
            w = cover_w if src.stem == "cover" else max_w
            notes.append(compress_image(src, dst, w, quality))
            if src.stem == "cover":
                cover = dst
            else:
                images.append(dst)
    if cover is None and not args.no_cover:
        print("FAIL: images/cover.jpg がない（--no-cover で動作確認は可能）")
        return 1

    # 章XHTML
    chapters = []  # (id, title, xhtml)
    for i, d in enumerate(drafts):
        md = d.read_text(encoding="utf-8")
        m = re.search(r"^#{1,2}\s+(.+)$", md, re.M)
        title = m.group(1).strip() if m else d.stem
        chapters.append((f"c{i:02d}", title, md_to_xhtml(md)))
    chapters.append(("back", "おわりに・奥付", back_matter_xhtml(meta, owarini_md)))

    # EPUB 組み立て
    out_dir = ROOT / "output"
    out_dir.mkdir(exist_ok=True)
    safe_title = re.sub(r"[^\w一-龠ぁ-んァ-ヶー]", "", meta["title"])[:20]
    epub_path = out_dir / f"{book.name[:3]}_{safe_title}.epub"
    uid = f"urn:chiju:{book.name}"
    pd = meta.get("publish_date") or date.today().isoformat()

    manifest, spine = [], []
    manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    manifest.append('<item id="css" href="style.css" media-type="text/css"/>')
    if cover:
        manifest.append('<item id="cover-img" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
        manifest.append('<item id="coverpage" href="cover.xhtml" media-type="application/xhtml+xml"/>')
        spine.append('<itemref idref="coverpage"/>')
    for cid, _, _ in chapters:
        manifest.append(f'<item id="{cid}" href="{cid}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{cid}"/>')
    for img in images:
        manifest.append(f'<item id="img-{img.stem}" href="images/{img.name}" media-type="image/jpeg"/>')

    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="ja">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{uid}</dc:identifier>
<dc:title>{html.escape(meta['title'])}</dc:title>
<dc:creator>{html.escape(meta['author'])}</dc:creator>
<dc:language>ja</dc:language>
<dc:date>{pd}</dc:date>
<meta property="dcterms:modified">{pd}T00:00:00Z</meta>
{'<meta name="cover" content="cover-img"/>' if cover else ''}
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine>
{chr(10).join(spine)}
</spine>
</package>
"""
    nav_items = "\n".join(
        f'<li><a href="{cid}.xhtml">{html.escape(t)}</a></li>' for cid, t, _ in chapters)
    nav = xhtml_doc("目次", f"""<nav epub:type="toc" id="toc"><h1>目次</h1>
<ol>
{nav_items}
</ol></nav>""")

    with zipfile.ZipFile(epub_path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>""", zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        if cover:
            z.write(cover, "OEBPS/images/cover.jpg", zipfile.ZIP_DEFLATED)
            z.writestr("OEBPS/cover.xhtml", xhtml_doc(
                meta["title"],
                '<p class="noindent"><img src="images/cover.jpg" alt="表紙"/></p>'),
                zipfile.ZIP_DEFLATED)
        for cid, title, body in chapters:
            z.writestr(f"OEBPS/{cid}.xhtml", xhtml_doc(title, body), zipfile.ZIP_DEFLATED)
        for img in images:
            z.write(img, f"OEBPS/images/{img.name}", zipfile.ZIP_DEFLATED)

    mb = epub_path.stat().st_size / 1048576
    print(f"生成: {epub_path.relative_to(ROOT)}（{mb:.2f}MB / 章 {len(chapters)}）")
    for n in notes:
        print(f"  画像: {n}")
    if mb > 3.5:
        print(f"FAIL: {mb:.2f}MB > 3.5MB（画像を減らす・圧縮率を上げる）")
        return 1
    if mb > max_mb:
        print(f"WARN: {mb:.2f}MB > 目安 {max_mb}MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
