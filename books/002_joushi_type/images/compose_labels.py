#!/usr/bin/env python3
"""002 画像合成: Gemini生成画像（文字なし）に表紙タイトル・図解ラベルを合成。
image_spec.md のラベル表が正。1冊目とグリッド・帯色を統一。
使い方: python3 compose_labels.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
SRC = HERE / "src"
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"
NAVY = (31, 58, 95)
WHITE = (255, 255, 255)


def font(size):
    return ImageFont.truetype(FONT, size)


def text(d, xy, s, size, fill, anchor="mm", bold=0):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=bold, stroke_fill=fill)


def multiline(d, xy, lines, size, fill, anchor="mm", bold=0, gap=1.25):
    x, y = xy
    for i, ln in enumerate(lines):
        oy = (i - (len(lines) - 1) / 2) * size * gap
        text(d, (x, y + oy), ln, size, fill, anchor, bold)


def compose_cover(src, out):
    img = Image.open(src).convert("RGB")
    img = img.resize((1600, round(img.height * 1600 / img.width)), Image.LANCZOS)
    if img.height < 2560:
        img = img.resize((1600, 2560), Image.LANCZOS)
    else:
        top = (img.height - 2560) // 2
        img = img.crop((0, top, 1600, top + 2560))
    d = ImageDraw.Draw(img, "RGBA")
    W, H = 1600, 2560
    # 上帯（シリーズ）: 半透明ネイビー帯
    d.rectangle([0, 0, W, 300], fill=NAVY + (235,))
    text(d, (W // 2, 155), "今夜の処方箋　02", 78, WHITE, bold=1)
    # 下帯（タイトル）: ネイビー帯を敷いて可読性を確保
    d.rectangle([0, 1800, W, H], fill=NAVY)
    text(d, (W // 2, 1990), "苦手な上司の", 166, WHITE, bold=2)
    text(d, (W // 2, 2175), "取扱説明書", 166, WHITE, bold=2)
    multiline(d, (W // 2, 2360),
              ["あなたの上司は5つの型のどれか。", "型が分かれば、急所が分かる。"],
              46, WHITE, bold=1, gap=1.3)
    text(d, (W - 70, 2495), "智珠", 50, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=86, optimize=True)


def open_diag(src, max_w=1200):
    img = Image.open(src).convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
    return img, ImageDraw.Draw(img), img.width, img.height


def ch01(src, out):  # 5型マップ（中心コンパス＋放射5・上下2段）
    img, d, W, H = open_diag(src)
    text(d, (W * .5, H * .625), "上司の5型", 19, NAVY, bold=1)
    cells = [
        (.5, .17, "高圧型", "軽く扱われる不安"),
        (.19, .50, "論破型", "間違いを認める恐れ"),
        (.81, .50, "マウント型", "価値がない恐れ"),
        (.32, .82, "被害者型", "無視される恐れ"),
        (.66, .82, "搾取型", "前例ができる恐れ"),
    ]
    for x, y, name, kyu in cells:
        text(d, (W * x, H * (y - .055)), name, 30, NAVY, bold=1)
        text(d, (W * x, H * (y + .05)), kyu, 19, NAVY)
    img.save(out, "JPEG", quality=82, optimize=True)


def before_after_3(src, out, head_l, head_r, left, right, foot=None,
                   lcolor=WHITE, rcolor=WHITE, rx=.73):
    """左右3ノードのBefore→After。左列/右列の中心x, 3段のy。
    ノード色は生成画像により異なる（濃色→WHITE字/淡色→NAVY字）。
    rx: 右列テキスト中心x（生成画像でノード左端に色タブがある場合は右へ寄せる）。"""
    img, d, W, H = open_diag(src)
    text(d, (W * .27, H * .10), head_l, 30, NAVY, bold=1)
    text(d, (W * rx, H * .10), head_r, 30, NAVY, bold=1)
    ys = [.215, .50, .785]
    for y, lines in zip(ys, left):
        multiline(d, (W * .27, H * y), lines, 23, lcolor, bold=1)
    for y, lines in zip(ys, right):
        multiline(d, (W * rx, H * y), lines, 23, rcolor, bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch02(src, out):  # Before全面降伏 / After記録の手
    before_after_3(
        Path(src), out, "Before: 全面降伏", "After: 記録の手",
        [["人前で怒鳴られる"], ["即座に「すみません」", "を連呼"], ["儀式が100%成立", "（次もあなた）"]],
        [["人前で怒鳴られる"], ["メモを取りつつ", "「事実だけ確認を」"], ["手応えを渡さない", "（足が遠のく）"]],
        lcolor=NAVY, rcolor=NAVY, rx=.77)


def ch03(src, out):  # 分岐: 議論→正しさ(相手へ)/決定(自分に)
    img, d, W, H = open_diag(src)
    text(d, (W * .5, H * .33), "詰め・指摘", 32, NAVY, bold=1)
    multiline(d, (W * .29, H * .66), ["〈何が正しいか〉", "正しさは相手へ渡す"], 24, NAVY, bold=1)
    multiline(d, (W * .71, H * .66), ["〈どう決めるか〉", "決定は手元に残す"], 24, WHITE, bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch04(src, out):  # Before採点 / After労い（火）
    before_after_3(
        Path(src), out, "Before: 採点で受ける", "After: 労いで受ける",
        [["自慢が始まる"], ["「すごいですね」", "（審判席に座る）"], ["格付け競技が続く", "（火が大きくなる）"]],
        [["自慢が始まる"], ["「そのころは", "大変だったんですね」"], ["昔話が閉じる", "（火が絞られる）"]])


def ch05(src, out):  # 境界線: 左2ノード（共感・礼儀）/停止バー/右1ノード（肩代わり）
    img, d, W, H = open_diag(src)
    multiline(d, (W * .25, H * .28), ["感情への共感", "「大変そうですね」"], 23, WHITE, bold=1)
    multiline(d, (W * .25, H * .72), ["礼儀", "「声かけてくださいね」"], 23, WHITE, bold=1)
    multiline(d, (W * .75, H * .50), ["業務の肩代わりはしない", "「じゃあ私がやります」"], 22, WHITE, bold=1)
    text(d, (W * .5, H * .40), "ここで止める", 20, NAVY, bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch06(src, out):  # 直線4フロー
    img, d, W, H = open_diag(src)
    boxes = [
        (.16, ["追加の押し付け", "が来る"], "金曜夕方の「ちょっと」"),
        (.39, ["抱えるA・Bを", "見せる"], "タスクの可視化"),
        (.62, ["「どちらを後ろ", "に回しますか」"], "入れ替え交渉"),
        (.85, ["順番の判断を", "上司に返す"], "断らずに境界が戻る"),
    ]
    for x, lines, note in boxes:
        multiline(d, (W * x, H * .47), lines, 22, WHITE, bold=1)
        text(d, (W * x, H * .66), note, 16, NAVY)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch07(src, out):  # サイクル5（中心=同じ一人）
    img, d, W, H = open_diag(src)
    text(d, (W * .5, H * .655), "同じ一人の上司", 20, NAVY, bold=1)
    ring = [(.5, .13, "高圧型"), (.80, .40, "論破型"), (.685, .80, "マウント型"),
            (.315, .80, "被害者型"), (.20, .40, "搾取型")]
    for x, y, name in ring:
        text(d, (W * x, H * y), name, 26, NAVY, bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


MAP = {
    "cover_main.png": ("cover.jpg", compose_cover),
    "ch01.png": ("ch01.jpg", ch01), "ch02.png": ("ch02.jpg", ch02),
    "ch03.png": ("ch03.jpg", ch03), "ch04.png": ("ch04.jpg", ch04),
    "ch05.png": ("ch05.jpg", ch05), "ch06.png": ("ch06.jpg", ch06),
    "ch07.png": ("ch07.jpg", ch07),
}

if __name__ == "__main__":
    for src_name, (out_name, fn) in MAP.items():
        src = SRC / src_name
        if not src.exists():
            print(f"SKIP: {src_name} なし")
            continue
        fn(src, HERE / out_name)
        print(f"OK: {src_name} → {out_name}")
