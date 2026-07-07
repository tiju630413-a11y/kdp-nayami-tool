#!/usr/bin/env python3
"""001 画像合成: Gemini生成画像（文字なし）に表紙タイトル・図解ラベルを合成する。

image_spec.md のラベル表が正。位置は各画像の実寸に対する比率で指定。
使い方: python3 compose_labels.py  （src/ に元画像、同階層に cover.jpg 等を出力）
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


def text(d, xy, s, size, fill, anchor="mm", bold=0, ls=None):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=bold, stroke_fill=fill, spacing=ls or size // 4)


def multiline(d, xy, lines, size, fill, anchor="mm", bold=0, gap=1.25):
    x, y = xy
    total = len(lines)
    for i, ln in enumerate(lines):
        oy = (i - (total - 1) / 2) * size * gap
        text(d, (x, y + oy), ln, size, fill, anchor, bold)


def compose_cover(src, out):
    img = Image.open(src).convert("RGB")
    img = img.resize((1600, round(img.height * 1600 / img.width)), Image.LANCZOS)
    if img.height < 2560:
        img = img.resize((1600, 2560), Image.LANCZOS)
    else:
        top = (img.height - 2560) // 2
        img = img.crop((0, top, 1600, top + 2560))
    d = ImageDraw.Draw(img)
    W, H = 1600, 2560
    # 上帯: シリーズ名
    text(d, (W // 2, 250), "今夜の処方箋　01", 78, WHITE, bold=1)
    # 下帯: タイトル2行＋サブ＋著者
    text(d, (W // 2, 2135), "職場の理不尽から", 168, WHITE, bold=5)
    text(d, (W // 2, 2320), "自分を守る台本50", 168, WHITE, bold=5)
    text(d, (W // 2, 2448), "言い返せなくていい。「守りの一言」だけ持っていく", 56, WHITE, bold=1)
    text(d, (W - 70, 2520), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.save(out, "JPEG", quality=86, optimize=True)


def open_diag(src, max_w=1200):
    img = Image.open(src).convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
    return img, ImageDraw.Draw(img), img.width, img.height


def ch01(src, out):
    img, d, W, H = open_diag(src)
    multiline(d, (W * .5, H * .235), ["① 同意しない"], 40, NAVY, bold=2)
    text(d, (W * .5, H * .292), "事実でない非を認めない", 22, NAVY)
    text(d, (W * .5, H * .645), "守りの一言", 36, NAVY, bold=2)
    multiline(d, (W * .28, H * .71), ["② 反撃しない"], 36, NAVY, bold=2)
    text(d, (W * .28, H * .765), "相手の優位を脅かさない", 20, NAVY)
    multiline(d, (W * .725, H * .715), ["③ 時間を稼ぐ"], 36, NAVY, bold=2)
    text(d, (W * .725, H * .77), "決着をあとへ持ち越す", 20, NAVY)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch02(src, out):
    img, d, W, H = open_diag(src)
    boxes = [
        (.153, ["会議で頭ごなし", "の否定"], "観客が最多＝儀式の土俵"),
        (.385, ["守りの一言で", "受ける"], "同意せず・反撃せず"),
        (.615, ["検証を会議の", "あとへ"], "土俵を後ろへずらす"),
        (.845, ["観客のいない場", "で事実を示す"], "準備の勝負に変わる"),
    ]
    for x, lines, note in boxes:
        multiline(d, (W * x, H * .5), lines, 27, WHITE, bold=1)
        multiline(d, (W * x, H * .625), [note[:11], note[11:]] if len(note) > 11 else [note],
                  18, NAVY)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch03(src, out):
    img, d, W, H = open_diag(src)
    text(d, (W * .5, H * .285), "人前の嫌味", 40, NAVY, bold=2)
    text(d, (W * .5, H * .35), "音量を絞った儀式", 22, NAVY)
    cols = [(.213, "気づかないふり", "D09・D11"), (.5, "受け流し", "D10・D12・D13"),
            (.787, "事実化", "D14・D15")]
    for x, name, ref in cols:
        text(d, (W * x, H * .70), name, 34, NAVY, bold=2)
        text(d, (W * x, H * .765), ref, 24, NAVY)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch04(src, out):
    img, d, W, H = open_diag(src)
    text(d, (W * .25, H * .045), "Before: 即答", 36, NAVY, bold=2)
    text(d, (W * .75, H * .045), "After: 保留", 36, NAVY, bold=2)
    left = [["金曜17時", "「今日中にできるよね？」"], ["即答「はい」"],
            ["押しつけ成立", "（週末が消える）"]]
    right = [["金曜17時", "「今日中にできるよね？」"],
             ["「量を見て判断したいので", "10分ください」"],
             ["量を測って条件の話へ", "（段取りの土俵）"]]
    ys = [.21, .50, .785]
    for y, lines in zip(ys, left):
        multiline(d, (W * .253, H * y), lines, 25, WHITE, bold=1)
    # 右列は1段目のみ紺地（白文字）、2・3段目は白地（紺文字）
    for y, lines, color in zip(ys, right, [WHITE, NAVY, NAVY]):
        multiline(d, (W * .753, H * y), lines, 25, color, bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch05(src, out):
    img, d, W, H = open_diag(src)
    text(d, (W * .27, H * .06), "謝罪のふたつの層", 36, NAVY, bold=2)
    multiline(d, (W * .27, H * .29), ["感情の層", "相手の気持ちに応える"], 30, NAVY, bold=1)
    multiline(d, (W * .27, H * .66), ["事実の層", "非を認めるかどうか"], 30, WHITE, bold=1)
    multiline(d, (W * .725, H * .30),
              ["短く応じる", "「ご心配をおかけした点は、", "申し訳ないと思っています」"],
              23, NAVY, bold=1)
    multiline(d, (W * .725, H * .675),
              ["経緯の確認に預ける", "「経緯は整理して、", "改めてご報告します」"],
              23, NAVY, bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch06(src, out):
    img, d, W, H = open_diag(src)
    text(d, (W * .5, H * .165), "5行のメモ（その日のうちに）", 34, WHITE, bold=1)
    rows = ["日時と場所", "相手の名前", "言われた言葉", "自分が返した言葉", "体に起きたこと"]
    ys = [.315, .425, .535, .648, .758]
    for y, s in zip(ys, rows):
        text(d, (W * .375, H * y), s, 28, NAVY, anchor="lm", bold=1)
    img.save(out, "JPEG", quality=82, optimize=True)


def ch07(src, out):
    img, d, W, H = open_diag(src)
    text(d, (W * .5, H * .055), "明日の自分に持たせる3枚のカード", 38, NAVY, bold=2)
    cards = [(.225, .60, 8, "守りの一言"), (.50, .58, 0, "二の手"),
             (.765, .60, -8, "自分との約束")]
    for x, y, ang, name in cards:
        # 回転テキストを透過レイヤで合成
        layer = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((200, 50), name, font=font(38), fill=WHITE + (255,),
                anchor="mm", stroke_width=1, stroke_fill=WHITE + (255,))
        layer = layer.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.paste(layer, (round(W * x - layer.width / 2),
                          round(H * y - layer.height / 2)), layer)
    img.save(out, "JPEG", quality=82, optimize=True)


LIGHT = (233, 238, 244)
GREY = (150, 162, 176)


def rbox(d, box, fill, radius=18, outline=None, width=0):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow_h(d, x0, x1, y, color=NAVY, w=7):
    d.line([(x0, y), (x1 - 14, y)], fill=color, width=w)
    d.polygon([(x1, y), (x1 - 18, y - 11), (x1 - 18, y + 11)], fill=color)


def gen_chat(out):
    """第7章: 文字の理不尽は、即答をしないだけで半分崩れる（3段フロー）。"""
    W, H = 1200, 720
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 70), "文字の理不尽は、即答をしないだけで半分崩れる", 40, NAVY, bold=1)
    cx = [200, 600, 1000]
    boxes = [
        (LIGHT, NAVY, ["相手の「今すぐ」"], "公開指摘・即レス催促・時間外"),
        (NAVY, WHITE, ["即答しない"], "こちらの時刻と場所を、一つ返す"),
        (LIGHT, NAVY, ["段取りに変わる"], "土俵は非公開・あなたの時間へ"),
    ]
    for i, (fill, fg, lines, note) in enumerate(boxes):
        x = cx[i]
        rbox(d, [x - 165, 210, x + 165, 380], fill, outline=NAVY, width=3)
        multiline(d, (x, 270), lines, 38, fg, bold=1)
        text(d, (x, 340), note, 21, fg if fill == NAVY else NAVY)
        if i < 2:
            arrow_h(d, cx[i] + 172, cx[i + 1] - 172, 295)
    rbox(d, [150, 470, 1050, 600], NAVY, radius=16)
    text(d, (W * .5, 512), "文字は、記録に残る。", 32, WHITE, bold=1)
    text(d, (W * .5, 560), "感情に反応せず事実だけ返せば、その記録はあとであなたを守る盾になる。", 24, WHITE)
    img.save(out, "JPEG", quality=84, optimize=True)


def gen_hyouka(out):
    """第8章: 評価の椅子では、主観を事実へ置き換える（2列変換表）。"""
    W, H = 1200, 760
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 62), "評価の椅子では、主観を事実へ置き換える", 40, NAVY, bold=1)
    lx, rx = 340, 860
    rbox(d, [70, 130, 610, 196], GREY, radius=12)
    rbox(d, [590, 130, 1130, 196], NAVY, radius=12)
    text(d, (lx, 163), "相手の主観（詰め）", 30, WHITE, bold=1)
    text(d, (rx, 163), "あなたが返す事実", 30, WHITE, bold=1)
    rows = [
        ("「期待外れだった」", "どの点がずれていたか、具体的に"),
        ("「やる気の問題だ」", "やる気ではなく、要因を整理したい"),
        ("「同期はできてる」", "私の課題として、次の優先は何か"),
        ("「もっと頑張って」", "評価が上がる条件を、一つでいい"),
    ]
    y = 220
    for i, (lft, rgt) in enumerate(rows):
        h = 108
        rbox(d, [70, y, 610, y + h], LIGHT if i % 2 else WHITE, radius=10, outline=GREY, width=2)
        rbox(d, [590, y, 1130, y + h], LIGHT if i % 2 else WHITE, radius=10, outline=NAVY, width=2)
        text(d, (lx, y + h / 2), lft, 27, NAVY, bold=1)
        arrow_h(d, 618, 648, y + h / 2, w=6)
        multiline(d, (rx, y + h / 2), _wrap(rgt), 25, NAVY, gap=1.2)
        y += h + 12
    text(d, (W * .5, 726), "言い負かさない。ただ、感想を具体へ、精神論を要因へ。", 24, NAVY)
    img.save(out, "JPEG", quality=84, optimize=True)


def _wrap(s):
    if len(s) <= 14:
        return [s]
    p = s.find("、")
    if 4 < p < len(s) - 3:
        return [s[:p + 1], s[p + 1:]]
    return [s[:len(s) // 2], s[len(s) // 2:]]


GEN = {"ch08_hyouka.jpg": gen_hyouka, "ch07_chat.jpg": gen_chat}


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
    for out_name, fn in GEN.items():
        fn(HERE / out_name)
        print(f"OK: (生成) → {out_name}")
