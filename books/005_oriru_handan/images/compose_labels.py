#!/usr/bin/env python3
"""005 図解生成: 純Pillowの作図。降りる判断（出口）の本。
表紙＝夜、社屋を出て一歩を踏み出す後ろ姿（外の光へ）。src/cover_main.png があれば合成。
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
LEAF = (86, 132, 112)     # 前向き・回復
DUSK = (198, 120, 96)     # 呪い・重い側
GLOW = (255, 214, 138)


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


def arrow_h(d, x0, x1, y, color=NAVY, w=7):
    d.line([(x0, y), (x1 - 14, y)], fill=color, width=w)
    d.polygon([(x1, y), (x1 - 18, y - 11), (x1 - 18, y + 11)], fill=color)


def person(d, cx, cy, s, color):
    d.ellipse([cx - s * .28, cy - s * .5, cx + s * .28, cy + s * .06], fill=color)
    d.rounded_rectangle([cx - s * .42, cy + s * .02, cx + s * .42, cy + s * .6], radius=s * .2, fill=color)


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
    W, H = 1600, 2560
    d.rectangle([0, 0, W, 250], fill=NAVY + (235,))
    text(d, (W // 2, 130), "今夜の処方箋　05", 74, WHITE, bold=1)
    d.rectangle([0, 1900, W, H], fill=(10, 16, 28, 232))
    multiline(d, (W // 2, 2100), ["職場の", "降り方"], 168, WHITE, bold=2, gap=1.2)
    multiline(d, (W // 2, 2380),
              ["逃げるは負けじゃない", "——削られる前に、自分を守って降りる"],
              44, (206, 216, 232), gap=1.35)
    text(d, (W - 80, 2500), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)


def cover(out):
    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(20 + t * 12), int(36 + t * 18), int(62 + t * 24)))
    d.rectangle([0, 0, W, 300], fill=NAVY + (235,))
    text(d, (W // 2, 155), "今夜の処方箋　05", 78, WHITE, bold=1)
    # ドアと外の光、出ていく後ろ姿
    rbox(d, [980, 700, 1360, 1500], (14, 22, 40, 255), radius=6)
    rbox(d, [1030, 760, 1310, 1440], GLOW + (60,), radius=4)   # ドアからの外の光
    d.rectangle([1030, 760, 1310, 1440], outline=(90, 110, 150, 255), width=6)
    for gx in range(0, 6):
        a = int(70 * (1 - gx / 6))
        d.rectangle([1030 - gx * 22, 760, 1310 + gx * 22, 1440], outline=GLOW + (a,), width=3)
    person(d, 760, 1180, 340, (206, 216, 232, 255))
    d.line([(180, 1470), (1400, 1470)], fill=(70, 90, 130, 255), width=5)
    text(d, (W // 2, 1600), "その扉から、出ていっていい", 44, (206, 216, 232), bold=1)
    d.rectangle([0, 1850, W, H], fill=(10, 16, 28, 236))
    multiline(d, (W // 2, 2050), ["職場の", "降り方"], 168, WHITE, bold=2, gap=1.2)
    multiline(d, (W // 2, 2340),
              ["逃げるは負けじゃない", "——削られる前に、自分を守って降りる"],
              44, (206, 216, 232), gap=1.35)
    text(d, (W - 80, 2485), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)


# ---------------- ch01 呪い→問い直し ----------------
def ch01(out):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "「逃げるは負け」の呪いを、問い直す", 40, NAVY, bold=1)
    rbox(d, [80, 150, 560, 560], WHITE, outline=DUSK, width=3)
    text(d, (320, 200), "呪いの言葉", 32, DUSK, bold=1)
    for i, s in enumerate(["「石の上にも三年」", "「逃げ癖がつく」", "「みんな我慢してる」"]):
        text(d, (320, 290 + i * 75), s, 25, INK)
    rbox(d, [640, 150, 1120, 560], WHITE, outline=LEAF, width=3)
    text(d, (880, 200), "三つの問い直し", 32, LEAF, bold=1)
    for i, s in enumerate(["これは本当か?", "誰の声だろう?", "守る言葉か、縛る言葉か?"]):
        text(d, (880, 290 + i * 75), s, 25, INK)
    arrow_h(d, 566, 634, 355, color=LEAF)
    rbox(d, [140, 600, 1060, 668], NAVY, radius=14)
    text(d, (W * .5, 634), "逃げるは、生き延びるための正当な防御", 26, WHITE, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch02 見極めフロー ----------------
def ch02(out):
    W, H = 1200, 760
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 56), "「降りていい」のサインを見分ける", 40, NAVY, bold=1)
    steps = [
        ("原因は変えられる？", "人手・繁忙・一時の相性なら、まだ守れる"),
        ("守りと回復を尽くした？", "01〜04の守り・03の回復を一度は試したか"),
        ("心身のサインは？", "2週間以上の不調・眠れない・朝動けない"),
    ]
    y = 130
    for i, (t, note) in enumerate(steps):
        rbox(d, [140, y, 1060, y + 96], LIGHT, radius=14, outline=NAVY, width=2)
        text(d, (170, y + 36), t, 29, NAVY, anchor="lm", bold=1)
        text(d, (170, y + 72), note, 22, INK, anchor="lm")
        if i < 2:
            arrow_down(d, 600, y + 100, y + 128)
        y += 158
    rbox(d, [300, y, 900, y + 78], DUSK, radius=16)
    multiline(d, (600, y + 39), ["尽くしても構造で削られ続ける", "＝降りる根拠"], 25, WHITE, bold=1, gap=1.25)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch03 降り方の段階マップ ----------------
def ch03(out):
    W, H = 1200, 720
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 56), "降り方には、段階がある（軽→重）", 40, NAVY, bold=1)
    steps = [
        ("① 距離を置く", "役割を返す・残業に線・有給"),
        ("② 配置換え・異動", "会社は替えず、場所を替える"),
        ("③ 休職", "籍を残し、いったん止まる"),
        ("④ 転職", "次を用意して、器を移す"),
        ("⑤ 退職", "完全に離れる（最後の一段）"),
    ]
    n = len(steps)
    for i, (t, note) in enumerate(steps):
        x = 110 + i * 42
        y = 560 - i * 92
        col = LEAF if i == 0 else (DUSK if i == 4 else NAVY)
        rbox(d, [x, y, x + 560, y + 82], col if i in (0, 4) else LIGHT, radius=12,
             outline=NAVY, width=2)
        c = WHITE if i in (0, 4) else NAVY
        text(d, (x + 24, y + 28), t, 26, c, anchor="lm", bold=1)
        text(d, (x + 24, y + 60), note, 20, c if i in (0, 4) else INK, anchor="lm")
    text(d, (W * .5, 682), "軽い段から。ただし心身が限界なら、上の段へ跳んでいい", 24, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch04 守って降りる準備リスト ----------------
def ch04(out):
    W, H = 1200, 680
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 56), "守って降りる——四つの準備", 40, NAVY, bold=1)
    text(d, (W * .5, 108), "まず「今日は、辞表を出さない」", 26, DUSK, bold=1)
    items = [
        ("① 記録を集める", "日時・事実・体の反応。降りる材料になる"),
        ("② 在職中に、次を見る", "求人を眺めるだけでも、視野が戻る"),
        ("③ 有給・引き継ぎを逆算", "降りる日から、後ろへたぐって組む"),
        ("④ 啖呵を切らない", "最後の一撃は、自分に返る。静かに降りる"),
    ]
    y = 160
    for t, note in items:
        rbox(d, [140, y, 1060, y + 96], WHITE, radius=14, outline=LEAF, width=2)
        text(d, (170, y + 36), t, 28, NAVY, anchor="lm", bold=1)
        text(d, (170, y + 72), note, 22, INK, anchor="lm")
        y += 116
    text(d, (W * .5, 646), "準備が、墜落を、着地に変える", 24, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch05 お金の見通し ----------------
def ch05(out):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 56), "お金の不安に、輪郭を引く三本の線", 40, NAVY, bold=1)
    lines = [
        ("① 毎月の最低生活費", "「いくら稼ぐ」でなく「いくらで生きられる」"),
        ("② 持ちこたえられる月数", "蓄え ÷ 最低生活費（自分の数字で）"),
        ("③ 使える制度と、下の床", "失業給付・傷病手当金／住居支援・生活保護"),
    ]
    y = 140
    for t, note in lines:
        rbox(d, [130, y, 1070, y + 100], LIGHT, radius=14, outline=NAVY, width=2)
        text(d, (160, y + 38), t, 29, NAVY, anchor="lm", bold=1)
        text(d, (160, y + 74), note, 22, INK, anchor="lm")
        y += 128
    rbox(d, [180, 560, 1020, 636], NAVY, radius=14)
    text(d, (W * .5, 598), "金額・条件は書かない。目安で“けた”をつかみ、公式で確認", 23, WHITE, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


GEN = {"ch01.jpg": ch01, "ch02.jpg": ch02, "ch03.jpg": ch03, "ch04.jpg": ch04, "ch05.jpg": ch05}

if __name__ == "__main__":
    base = None
    for cand in ("cover_main.png", "cover_spare.png"):
        if (HERE / "src" / cand).exists():
            base = HERE / "src" / cand
            break
    if base:
        compose_cover_over_base(base, HERE / "cover.jpg")
        print(f"OK: cover.jpg（Gemini下地 {base.name} に合成）")
    else:
        cover(HERE / "cover.jpg")
        print("OK: cover.jpg（純Pillow・下地なし）")
    for name, fn in GEN.items():
        fn(HERE / name)
        print(f"OK: {name}")
