#!/usr/bin/env python3
"""006 図解生成: 純Pill275ドの作図。中間管理職の板挟み（縦の上下）を守る本。
表紙＝上下の矢印に挟まれても潰れず立つ人物。src/cover_main.png があれば合成。
使い方: python3 compose_labels.py
図: ch01 通す/止める/返す三分法 / ch02 上の無理→事実で整えて返す /
    ch03 傾聴と肩代わりの分離 / ch04 酸素マスクの順番 /
    ch05 抱え込み→任せる・断る・上げる / maki 巻末早見表
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
LEAF = (86, 132, 112)     # 守り・受ける・任せる
DUSK = (198, 120, 96)     # 無理・刃・抱え込み
GLOW = (255, 214, 138)
SKY = (108, 146, 190)     # 上


def font(size):
    return ImageFont.truetype(FONT, size)


def text(d, xy, s, size, fill, anchor="mm", bold=0):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor, stroke_width=bold, stroke_fill=fill)


def multiline(d, xy, lines, size, fill, anchor="mm", bold=0, gap=1.28):
    x, y = xy
    for i, ln in enumerate(lines):
        text(d, (x, y + (i - (len(lines) - 1) / 2) * size * gap), ln, size, fill, anchor, bold)


def rbox(d, box, fill, radius=18, outline=None, width=0):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow_down(d, x, y0, y1, color=NAVY, w=7):
    d.line([(x, y0), (x, y1 - 14)], fill=color, width=w)
    d.polygon([(x, y1), (x - 11, y1 - 18), (x + 11, y1 - 18)], fill=color)


def arrow_up(d, x, y0, y1, color=NAVY, w=7):
    d.line([(x, y0), (x, y1 + 14)], fill=color, width=w)
    d.polygon([(x, y1), (x - 11, y1 + 18), (x + 11, y1 + 18)], fill=color)


def arrow_h(d, x0, x1, y, color=NAVY, w=7):
    d.line([(x0, y), (x1 - 14, y)], fill=color, width=w)
    d.polygon([(x1, y), (x1 - 18, y - 11), (x1 - 18, y + 11)], fill=color)


def person(d, cx, cy, s, color):
    d.ellipse([cx - s * .28, cy - s * .5, cx + s * .28, cy + s * .06], fill=color)
    d.rounded_rectangle([cx - s * .42, cy + s * .02, cx + s * .42, cy + s * .6], radius=s * .2, fill=color)


W, H = 1600, 1000


def canvas():
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img, "RGBA")


def save(img, name):
    img.convert("RGB").save(HERE / name, "JPEG", quality=88, optimize=True)


# ---------------- ch01 通す/止める/返す 三分法 ----------------
def fig_ch01():
    img, d = canvas()
    text(d, (W // 2, 70), "降ってきた要求を、三つに選り分ける", 52, INK, bold=1)
    # 上からの要求
    rbox(d, [610, 140, 990, 250], NAVY, radius=16)
    multiline(d, (800, 195), ["上から降ってきた", "要求・数字・締切"], 38, WHITE)
    arrow_down(d, 800, 250, 320, color=NAVY)
    rbox(d, [640, 320, 960, 430], LIGHT, radius=16, outline=NAVY, width=3)
    multiline(d, (800, 375), ["いったん", "受け止めて選り分ける"], 34, INK)
    # 三分岐
    ys = 620
    cols = [
        (300, LEAF, "通す", ["そのまま", "下へ渡してよいもの"]),
        (800, NAVY, "止める", ["自分のところで止め、", "下に流さない"]),
        (1300, DUSK, "返す", ["条件をつけて", "上へ差し戻す"]),
    ]
    d.line([(300, 460), (1300, 460)], fill=NAVY, width=5)
    for x, c, head, sub in cols:
        d.line([(x, 430), (x, 460)], fill=NAVY, width=5)
        arrow_down(d, x, 460, ys - 90, color=c)
        rbox(d, [x - 210, ys - 80, x + 210, ys + 110], WHITE, radius=18, outline=c, width=4)
        text(d, (x, ys - 30), head, 46, c, bold=1)
        multiline(d, (x, ys + 55), sub, 30, INK)
    # 下段: 緩衝材との対比
    rbox(d, [140, 800, 1460, 940], (250, 238, 232), radius=16, outline=DUSK, width=3)
    multiline(d, (800, 870),
              ["反射で「全部を通す」と、あなたは緩衝材になり、先に擦り切れる。",
               "三つに選り分けることが、板挟みで潰れないための最初の守り。"],
              32, INK, gap=1.35)
    save(img, "ch01.jpg")


# ---------------- ch02 上の無理→事実で整えて返す ----------------
def fig_ch02():
    img, d = canvas()
    text(d, (W // 2, 70), "上の無理を、事実で整えてから扱う", 52, INK, bold=1)
    # 左: 無理（勢い）
    rbox(d, [90, 300, 400, 560], (250, 238, 232), radius=18, outline=DUSK, width=4)
    multiline(d, (245, 400), ["上の無理", "（勢い・数字・締切）"], 34, DUSK, bold=1)
    text(d, (245, 500), "そのまま飲むと×", 30, DUSK)
    arrow_h(d, 400, 560, 430, color=NAVY)
    # 中: 五つの型
    rbox(d, [575, 180, 1035, 700], WHITE, radius=20, outline=NAVY, width=4)
    text(d, (805, 235), "翻訳する五本", 40, NAVY, bold=1)
    items = ["① 即答しない（確認して折り返す）",
             "② 事実で返す（工数・人員）",
             "③ 条件を差し出す（削ればできる）",
             "④ 優先順位を上に決めてもらう",
             "⑤ 決めたことを記録に残す"]
    for i, s in enumerate(items):
        y = 305 + i * 76
        text(d, (610, y), s, 30, INK, anchor="lm")
    arrow_h(d, 1035, 1195, 430, color=LEAF)
    # 右: 動かせる形
    rbox(d, [1200, 300, 1510, 560], (232, 244, 238), radius=18, outline=LEAF, width=4)
    multiline(d, (1355, 400), ["現場で", "動かせる形"], 34, LEAF, bold=1)
    text(d, (1355, 500), "下へ渡せる○", 30, LEAF)
    rbox(d, [140, 810, 1460, 930], (240, 245, 251), radius=16, outline=NAVY, width=2)
    text(d, (800, 870), "全部を薄めて下へ丸投げしない。翻訳する人がいる階で、無理の連鎖は止まる。", 31, INK)
    save(img, "ch02.jpg")


# ---------------- ch03 傾聴と肩代わりの分離 ----------------
def fig_ch03():
    img, d = canvas()
    text(d, (W // 2, 70), "傾聴はする。肩代わりはしない。", 52, INK, bold=1)
    # 部下から
    rbox(d, [610, 140, 990, 250], NAVY, radius=16)
    multiline(d, (800, 195), ["部下からの", "相談・不満・トラブル"], 36, WHITE)
    # 分離線
    d.line([(800, 250), (800, 330)], fill=NAVY, width=5)
    arrow_down(d, 470, 350, 430, color=LEAF)
    arrow_down(d, 1130, 350, 430, color=NAVY)
    d.line([(470, 330), (1130, 330)], fill=NAVY, width=5)
    d.line([(800, 250), (800, 330)], fill=NAVY, width=5)
    # 左: 気持ち＝受ける
    rbox(d, [180, 440, 760, 720], (232, 244, 238), radius=18, outline=LEAF, width=4)
    text(d, (470, 500), "気持ち", 44, LEAF, bold=1)
    text(d, (470, 560), "○ 受け止める（傾聴）", 32, INK)
    multiline(d, (470, 645), ["「それは大変だったね」", "と、まず聞く"], 30, INK)
    # 右: 課題＝戻す
    rbox(d, [840, 440, 1420, 720], (250, 238, 232), radius=18, outline=DUSK, width=4)
    text(d, (1130, 500), "課題", 44, DUSK, bold=1)
    text(d, (1130, 560), "× 肩代わりしない", 32, INK)
    multiline(d, (1130, 645), ["本人・組織の役割へ戻す。", "解決を全部は引き受けない"], 29, INK)
    # 下: 抱え込みとの対比
    rbox(d, [140, 810, 1460, 930], (250, 238, 232), radius=16, outline=DUSK, width=3)
    text(d, (800, 870), "線を引かず全部を自分の側へ引き受けると、あなたが先に潰れ、部下も育たない。", 31, INK)
    save(img, "ch03.jpg")


# ---------------- ch04 酸素マスクの順番 ----------------
def fig_ch04():
    img, d = canvas()
    text(d, (W // 2, 80), "酸素マスクは、まず自分から", 52, INK, bold=1)
    # ①自分
    rbox(d, [200, 250, 720, 620], (232, 244, 238), radius=22, outline=LEAF, width=5)
    text(d, (460, 320), "①  まず自分", 46, LEAF, bold=1)
    person(d, 460, 470, 150, LEAF)
    text(d, (460, 585), "自分が酸素を吸う", 30, INK)
    arrow_h(d, 720, 880, 435, color=NAVY, w=9)
    text(d, (800, 390), "その次に", 30, INK)
    # ②部下
    rbox(d, [880, 250, 1400, 620], (240, 245, 251), radius=22, outline=NAVY, width=5)
    text(d, (1140, 320), "②  部下", 46, NAVY, bold=1)
    person(d, 1075, 470, 120, NAVY)
    person(d, 1210, 470, 120, SKY)
    text(d, (1140, 585), "隣の人にもつけてやれる", 30, INK)
    rbox(d, [140, 730, 1460, 920], (240, 245, 251), radius=16, outline=NAVY, width=2)
    multiline(d, (800, 825),
              ["自分を守ることと、部下を守ることは、対立しない。ただの順番だ。",
               "自分が先に倒れたら、誰も守れない。だから、まず自分の酸素マスクを。"],
              32, INK, gap=1.4)
    save(img, "ch04.jpg")


# ---------------- ch05 抱え込み→任せる・断る・上げる ----------------
def fig_ch05():
    img, d = canvas()
    text(d, (W // 2, 70), "抱え込みを、三方向へ分散する", 52, INK, bold=1)
    # 中央: 抱え込む自分
    person(d, 800, 470, 150, NAVY)
    rbox(d, [690, 300, 910, 380], (250, 238, 232), radius=12, outline=DUSK, width=3)
    text(d, (800, 340), "全部が集まる", 28, DUSK)
    text(d, (800, 610), "あなた（結節点）", 30, INK)
    # 上げる（上へ）
    arrow_up(d, 800, 300, 175, color=DUSK, w=8)
    rbox(d, [560, 90, 1040, 175], (250, 238, 232), radius=16, outline=DUSK, width=4)
    multiline(d, (800, 132), ["上げる — 上司・他部署・人事へ"], 32, DUSK, bold=1)
    # 任せる（下へ）
    arrow_down(d, 560, 540, 780, color=LEAF, w=8)
    rbox(d, [300, 790, 780, 910], (232, 244, 238), radius=16, outline=LEAF, width=4)
    multiline(d, (540, 850), ["任せる — 部下・チームへ"], 32, LEAF, bold=1)
    # 断る・返す（横／上へ条件）
    arrow_h(d, 950, 1180, 470, color=NAVY, w=8)
    rbox(d, [1180, 400, 1520, 545], (240, 245, 251), radius=16, outline=NAVY, width=4)
    multiline(d, (1350, 472), ["断る・返す", "上へ条件をつけて"], 31, NAVY, bold=1)
    rbox(d, [140, 940, 1460, 995], (240, 245, 251), radius=12)
    text(d, (800, 968), "抱え込みは美徳ではなく、組織のボトルネック化。一人に全部を集めない。", 30, INK)
    save(img, "ch05.jpg")


# ---------------- 巻末 板挟みの守り 早見表図 ----------------
def fig_maki():
    img = Image.new("RGB", (1600, 1180), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    text(d, (800, 70), "板挟みの守り 早見表", 56, NAVY, bold=1)
    rows = [
        ("向き", "場面", "守りの一手"),
        ("構造", "板挟みで消耗している", "力不足でなく構造。緩衝材を全部は引き受けない"),
        ("上へ", "無理な数字・締切が降ってきた", "即答しない／事実で返す／条件・優先順位を上へ返す"),
        ("下へ", "部下の相談・不満・トラブル", "気持ちは受け止める。課題は本人・組織へ戻す"),
        ("自分", "手が回らない・気力が尽きる", "まず自分の酸素マスク。境界を引く。完璧をやめる"),
        ("実装", "全部を自分で抱えている", "任せる・NOと言う（返す）・上げる の三方向へ"),
        ("場面", "注意・評価・正面衝突", "人格でなく事実と基準で。余裕がない時ほど言い方に注意"),
        ("限界", "眠れない・消えたいがよぎる", "二週間を待たない。相談先・緊急ルートへ（第7章）"),
    ]
    x0, x1, x2, x3 = 90, 320, 760, 1510
    y = 150
    rh = 122
    for i, (a, b, c) in enumerate(rows):
        head = (i == 0)
        fill = NAVY if head else (WHITE if i % 2 else LIGHT)
        d.rectangle([x0, y, x3, y + (90 if head else rh)], fill=fill)
        tc = WHITE if head else INK
        hh = 90 if head else rh
        text(d, ((x0 + x1) // 2, y + hh // 2), a, 32 if head else 34, tc, bold=1 if head else 0)
        text(d, (x1 + 24, y + hh // 2), b, 28 if head else 30, tc, anchor="lm")
        # 折り返し対応: 守りの一手が長い場合、そのまま1行で（フォント小さめ）
        text(d, (x2 + 24, y + hh // 2), c, 26 if head else 28, tc, anchor="lm")
        y += (90 if head else rh)
    d.rectangle([x0, 150, x3, y], outline=NAVY, width=3)
    for xx in (x1, x2):
        d.line([(xx, 150), (xx, y)], fill=NAVY, width=2)
    text(d, (800, y + 45), "順番は、いつも「まず自分」。あなたが壊れないことが、いちばんのマネジメント。", 30, INK)
    img.convert("RGB").save(HERE / "maki.jpg", "JPEG", quality=88, optimize=True)


# ---------------- 表紙 ----------------
def compose_cover_over_base(src, out):
    img = Image.open(src).convert("RGB")
    img = img.resize((1600, round(img.height * 1600 / img.width)), Image.LANCZOS)
    if img.height < 2560:
        img = img.resize((1600, 2560), Image.LANCZOS)
    else:
        top = (img.height - 2560) // 2
        img = img.crop((0, top, 1600, top + 2560))
    d = ImageDraw.Draw(img, "RGBA")
    CW, CH = 1600, 2560
    d.rectangle([0, 0, CW, 250], fill=NAVY + (235,))
    text(d, (CW // 2, 130), "今夜の処方箋　06", 74, WHITE, bold=1)
    d.rectangle([0, 1880, CW, CH], fill=(10, 16, 28, 232))
    multiline(d, (CW // 2, 2090), ["中間管理職の", "身の守り方"], 150, WHITE, bold=2, gap=1.22)
    multiline(d, (CW // 2, 2380),
              ["上と下の板挟みで、", "あなたが先に潰れないために"],
              46, (206, 216, 232), gap=1.35)
    text(d, (CW - 80, 2500), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)


def cover(out):
    CW, CH = 1600, 2560
    img = Image.new("RGB", (CW, CH), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    for yy in range(CH):
        t = yy / CH
        d.line([(0, yy), (CW, yy)], fill=(int(20 + t * 12), int(36 + t * 18), int(62 + t * 24)))
    d.rectangle([0, 0, CW, 300], fill=NAVY + (235,))
    text(d, (CW // 2, 155), "今夜の処方箋　06", 78, WHITE, bold=1)
    # 上下の矢印に挟まれても潰れず立つ人物
    cx, cy = 800, 1180
    arrow_down(d, cx, 720, 1000, color=DUSK, w=16)
    arrow_up(d, cx, 1640, 1360, color=SKY, w=16)
    text(d, (cx, 690), "上の無理", 54, (232, 200, 190), bold=1)
    text(d, (cx, 1690), "下の現実", 54, (200, 214, 236), bold=1)
    person(d, cx, cy, 320, WHITE)
    # 足場
    d.line([(cx - 220, cy + 200), (cx + 220, cy + 200)], fill=GLOW, width=10)
    d.rectangle([0, 1900, CW, CH], fill=(10, 16, 28, 232))
    multiline(d, (CW // 2, 2110), ["中間管理職の", "身の守り方"], 150, WHITE, bold=2, gap=1.22)
    multiline(d, (CW // 2, 2400),
              ["上と下の板挟みで、", "あなたが先に潰れないために"],
              46, (206, 216, 232), gap=1.35)
    text(d, (CW - 80, 2510), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)


if __name__ == "__main__":
    fig_ch01()
    fig_ch02()
    fig_ch03()
    fig_ch04()
    fig_ch05()
    fig_maki()
    src = HERE / "src" / "cover_main.png"
    if src.exists():
        compose_cover_over_base(src, HERE / "cover.jpg")
        print("cover: composed over base")
    else:
        cover(HERE / "cover.jpg")
        print("cover: Pillow fallback")
    print("done: ch01-ch05, maki, cover")
