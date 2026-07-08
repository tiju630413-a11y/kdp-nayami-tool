#!/usr/bin/env python3
"""003 図解生成: 純Pillowの作図（Gemini下地なし）。回復編にふさわしい静かな夜の意匠。
表紙＝夜の自室・ベッドサイドの灯り。01/02とネイビー基調を統一。
使い方: python3 compose_labels.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"
NAVY = (31, 58, 95)
INK = (38, 46, 60)
WHITE = (255, 255, 255)
PAPER = (247, 249, 252)
LIGHT = (233, 238, 244)
GREY = (150, 162, 176)
GLOW = (255, 214, 138)      # ベッドサイドの灯り
LEAF = (86, 132, 112)       # 回復（緑）
DUSK = (198, 120, 96)       # 逃避（くすんだ橙）


def font(size):
    return ImageFont.truetype(FONT, size)


def text(d, xy, s, size, fill, anchor="mm", bold=0):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=bold, stroke_fill=fill)


def multiline(d, xy, lines, size, fill, anchor="mm", bold=0, gap=1.28):
    x, y = xy
    for i, ln in enumerate(lines):
        oy = (i - (len(lines) - 1) / 2) * size * gap
        text(d, (x, y + oy), ln, size, fill, anchor, bold)


def rbox(d, box, fill, radius=18, outline=None, width=0):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow_down(d, x, y0, y1, color=NAVY, w=7):
    d.line([(x, y0), (x, y1 - 14)], fill=color, width=w)
    d.polygon([(x, y1), (x - 11, y1 - 18), (x + 11, y1 - 18)], fill=color)


def arrow_h(d, x0, x1, y, color=NAVY, w=7):
    d.line([(x0, y), (x1 - 14, y)], fill=color, width=w)
    d.polygon([(x1, y), (x1 - 18, y - 11), (x1 - 18, y + 11)], fill=color)


# ---------------- 表紙 ----------------
def cover(out):
    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), (14, 20, 34))
    d = ImageDraw.Draw(img, "RGBA")
    # 夜空のグラデーション（上=濃紺→下=藍）
    for y in range(H):
        t = y / H
        r = int(14 + t * 20)
        g = int(20 + t * 30)
        b = int(34 + t * 46)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # ベッドサイドの灯り（右下の温かい放射）
    cx, cy = 1180, 1720
    for rad in range(520, 0, -8):
        a = int(52 * (1 - rad / 520) ** 2)
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=GLOW + (a,))
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=GLOW + (235,))
    # ランプの支柱と台
    d.rectangle([cx - 6, cy + 30, cx + 6, cy + 220], fill=(60, 66, 82, 255))
    d.rectangle([cx - 70, cy + 220, cx + 70, cy + 240], fill=(60, 66, 82, 255))
    # 窓枠（左上の薄明かり）
    rbox(d, [150, 360, 560, 900], (28, 38, 60, 255), radius=8)
    d.line([(355, 360), (355, 900)], fill=(60, 74, 104, 255), width=6)
    d.line([(150, 630), (560, 630)], fill=(60, 74, 104, 255), width=6)
    # 上帯（シリーズ）
    d.rectangle([0, 0, W, 250], fill=NAVY + (235,))
    text(d, (W // 2, 130), "今夜の処方箋　03", 74, WHITE, bold=1)
    # タイトル（下部・可読の帯）
    d.rectangle([0, 1900, W, H], fill=(10, 16, 28, 232))
    multiline(d, (W // 2, 2110),
              ["言い返せなかった夜の、", "心の片づけ方"], 138, WHITE, bold=2, gap=1.22)
    multiline(d, (W // 2, 2360),
              ["反芻して眠れない夜を、", "そっと手放すために"],
              50, (206, 216, 232), bold=0, gap=1.3)
    text(d, (W - 80, 2495), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.save(out, "JPEG", quality=88, optimize=True)


# ---------------- ch01 反芻＝昼の宿題が夜に開く ----------------
def ch01(out):
    W, H = 1200, 720
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 62), "反芻は、弱さではなく“未処理の宿題”", 42, NAVY, bold=1)
    # 昼パネル
    rbox(d, [80, 150, 560, 560], WHITE, outline=GREY, width=3)
    text(d, (320, 200), "昼", 40, NAVY, bold=1)
    text(d, (320, 250), "処理しきれない一言が積まれる", 24, INK)
    for i, lab in enumerate(["否定された", "詰められた", "返せなかった"]):
        y = 320 + i * 70
        rbox(d, [140, y, 500, y + 52], LIGHT, radius=10)
        text(d, (320, y + 26), lab, 24, NAVY, bold=1)
    # 夜パネル
    rbox(d, [640, 150, 1120, 560], (20, 30, 52), radius=18)
    text(d, (880, 200), "夜", 40, GLOW, bold=1)
    text(d, (880, 250), "静かになって、宿題が“開く”", 24, (210, 220, 236))
    for i, lab in enumerate(["再生", "反芻", "眠れない"]):
        y = 320 + i * 70
        rbox(d, [700, y, 1060, y + 52], (36, 48, 74), radius=10)
        text(d, (880, y + 26), lab, 24, GLOW, bold=1)
    arrow_h(d, 566, 634, 355)
    rbox(d, [140, 610, 1060, 686], NAVY, radius=14)
    text(d, (W * .5, 648), "根性で止めず、頭の外へ出す——これが全編の芯", 25, WHITE, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch03 5要素分解＋言い換え ----------------
def ch03(out):
    W, H = 1200, 780
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "団子を、事実と感情に切り分ける", 42, NAVY, bold=1)
    rows = [
        ("①出来事", "木曜夕方、会議室で", 0),
        ("②言われた言葉", "「なんでできないの」", 0),
        ("③返した言葉", "「すみません」", 0),
        ("④体に起きたこと", "手が震え、頭が白く", 0),
        ("⑤わいた解釈", "だから私はダメだ", 1),
    ]
    y = 130
    for tag, val, is_kai in rows:
        col = DUSK if is_kai else NAVY
        rbox(d, [80, y, 360, y + 78], col, radius=12)
        text(d, (220, y + 39), tag, 27, WHITE, bold=1)
        rbox(d, [372, y, 760, y + 78], WHITE, radius=12, outline=GREY, width=2)
        text(d, (566, y + 39), val, 26, INK)
        y += 92
    # 言い換え矢印＋変換
    text(d, (960, 150), "⑤だけを言い換える", 24, DUSK, bold=1)
    rbox(d, [800, 210, 1130, 300], LIGHT, radius=12)
    text(d, (965, 255), "私はいつもダメだ", 26, DUSK, bold=1)
    # 下向き矢印
    d.line([(965, 312), (965, 356)], fill=LEAF, width=8)
    d.polygon([(965, 372), (952, 350), (978, 350)], fill=LEAF)
    rbox(d, [800, 384, 1130, 474], LEAF, radius=12)
    multiline(d, (965, 429), ["今日、この一言が", "言えなかった"], 25, WHITE, bold=1)
    rbox(d, [80, 690, 1120, 758], NAVY, radius=14)
    text(d, (W * .5, 724), "事実は小さい。膨らむのは、いつも⑤の解釈のほう。", 26, WHITE, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch04 切り替えスイッチ 逃避×回復 ----------------
def ch04(out):
    W, H = 1200, 740
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "切り替えスイッチ——逃避と、回復は違う", 42, NAVY, bold=1)
    # 逃避（左）
    rbox(d, [80, 140, 570, 660], WHITE, outline=DUSK, width=3)
    text(d, (325, 190), "ただ忘れる逃避", 34, DUSK, bold=1)
    text(d, (325, 240), "酒・夜更かし・スマホ", 24, INK)
    for i, lab in enumerate(["麻痺させて先送り", "記録がないと戻る", "翌朝をさらに削る"]):
        y = 300 + i * 92
        rbox(d, [130, y, 520, y + 66], (247, 235, 230), radius=12)
        text(d, (325, y + 33), lab, 25, DUSK, bold=1)
    # 回復（右）
    rbox(d, [630, 140, 1120, 660], WHITE, outline=LEAF, width=3)
    text(d, (875, 190), "回復としての切り替え", 34, LEAF, bold=1)
    text(d, (875, 240), "温泉・サウナ・映画・散歩", 24, INK)
    for i, lab in enumerate(["まず記録して外へ出す", "体をほどいて閉じる", "翌朝を削らない"]):
        y = 300 + i * 92
        rbox(d, [680, y, 1070, y + 66], (230, 242, 236), radius=12)
        text(d, (875, y + 33), lab, 25, LEAF, bold=1)
    text(d, (W * .5, 700), "順番は、記録が先。そのあとに、体をほどく。", 26, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch05 寝る前3分・4ステップ ----------------
def ch05(out):
    W, H = 1200, 760
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 60), "寝る前の3分、四つの手順", 42, NAVY, bold=1)
    steps = [
        ("①", "今日の五行を書く", "頭の中身を、画面へ出す"),
        ("②", "自責を、事実の一行へ", "「いつも」を「今日」に"),
        ("③", "明日の自分に一行", "ねぎらい、または一手"),
        ("④", "脳内の相手を手放す", "画面を伏せ、長く息を吐く"),
    ]
    y = 150
    for num, title, note in steps:
        rbox(d, [90, y, 190, y + 108], NAVY, radius=16)
        text(d, (140, y + 54), num, 46, WHITE, bold=2)
        rbox(d, [210, y, 1110, y + 108], WHITE, radius=14, outline=GREY, width=2)
        text(d, (245, y + 42), title, 32, NAVY, anchor="lm", bold=1)
        text(d, (245, y + 80), note, 24, INK, anchor="lm")
        if num != "④":
            arrow_down(d, 140, y + 112, y + 140)
        y += 148
    text(d, (W * .5, 730), "降ろす・ほどく・渡す・閉じる。全部できない夜は、④だけでいい。", 25, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch06 守れた夜カレンダー ----------------
def ch06(out):
    W, H = 1200, 760
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 60), "“守れた夜”を数える", 42, NAVY, bold=1)
    text(d, (W * .5, 118), "反芻ゼロでなく、手を一つ打てた夜に◯", 26, INK)
    # カレンダー4週×7日
    marks = {  # (week,row)->type: 0=なし,1=◯,2=半分◯
        (0, 1): 1, (0, 3): 2, (0, 5): 1,
        (1, 0): 1, (1, 2): 1, (1, 3): 1, (1, 6): 2,
        (2, 1): 1, (2, 2): 2, (2, 4): 1, (2, 5): 1, (2, 6): 1,
        (3, 0): 2, (3, 1): 1, (3, 3): 1, (3, 4): 1, (3, 5): 1, (3, 6): 1,
    }
    days = ["月", "火", "水", "木", "金", "土", "日"]
    x0, y0, cw, ch = 160, 190, 120, 118
    for j, dlab in enumerate(days):
        text(d, (x0 + j * cw + cw / 2, y0 - 24), dlab, 26, NAVY, bold=1)
    for wk in range(4):
        for dy in range(7):
            x = x0 + dy * cw
            y = y0 + wk * ch
            rbox(d, [x + 6, y + 6, x + cw - 6, y + ch - 6], WHITE, radius=12,
                 outline=LIGHT, width=2)
            m = marks.get((wk, dy), 0)
            cx, cy = x + cw / 2, y + ch / 2
            if m == 1:
                d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=LEAF, width=8)
            elif m == 2:
                d.arc([cx - 30, cy - 30, cx + 30, cy + 30], 90, 270, fill=LEAF, width=8)
    text(d, (W * .5, 726), "週末に数を数える。半分できた夜も、一勝に入れていい。", 25, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


GEN = {
    "cover.jpg": cover,
    "ch01.jpg": ch01, "ch03.jpg": ch03, "ch04.jpg": ch04,
    "ch05.jpg": ch05, "ch06.jpg": ch06,
}

if __name__ == "__main__":
    for name, fn in GEN.items():
        fn(HERE / name)
        print(f"OK: {name}")
