#!/usr/bin/env python3
"""004 図解生成: 純Pillowの作図（Gemini下地なし）。関係を勾配で見分ける本の図解。
表紙＝ネイビー基調・“横並び”のモチーフ（02の見上げる上司に対し、同じ目線の複数）。
使い方: python3 compose_labels.py
表紙のGemini下地 src/cover_main.png があれば、それに文字帯を合成する。
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
LEAF = (86, 132, 112)     # 横＝線を引ける（前向き）
DUSK = (198, 120, 96)     # 効かない側／縦の坂


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


def person(d, cx, cy, s, color):
    """簡単な人型シルエット（頭＋肩）。"""
    d.ellipse([cx - s * .28, cy - s * .5, cx + s * .28, cy + s * .06], fill=color)
    d.rounded_rectangle([cx - s * .42, cy + s * .02, cx + s * .42, cy + s * .6],
                        radius=s * .2, fill=color)


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
    text(d, (W // 2, 130), "今夜の処方箋　04", 74, WHITE, bold=1)
    d.rectangle([0, 1900, W, H], fill=(10, 16, 28, 232))
    multiline(d, (W // 2, 2090), ["職場の困った人の", "取扱説明書"], 150, WHITE, bold=2, gap=1.2)
    multiline(d, (W // 2, 2360),
              ["同僚・後輩・取引先", "——上司じゃない相手の守り方"],
              48, (206, 216, 232), gap=1.35)
    text(d, (W - 80, 2495), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)


def cover(out):
    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(24 + t * 14), int(44 + t * 20), int(74 + t * 26)))
    # 上帯
    d.rectangle([0, 0, W, 300], fill=NAVY + (235,))
    text(d, (W // 2, 155), "今夜の処方箋　04", 78, WHITE, bold=1)
    # 中央：横並びの4人（同じ目線＝勾配なし）＋足元に一本の水平線
    ppl = [(W * .22, "同僚"), (W * .40, "後輩"), (W * .60, "取引先"), (W * .78, "他部署")]
    y0 = 1150
    for x, lab in ppl:
        person(d, x, y0, 260, (210, 220, 236, 255))
        text(d, (x, y0 + 210), lab, 40, (210, 220, 236), bold=1)
    d.line([(180, y0 + 300), (W - 180, y0 + 300)], fill=(150, 200, 175, 255), width=6)
    text(d, (W // 2, y0 + 350), "みな、同じ目線に並んでいる", 40, (150, 200, 175), bold=1)
    # 下帯：タイトル
    d.rectangle([0, 1850, W, H], fill=(10, 16, 28, 236))
    multiline(d, (W // 2, 2040), ["職場の困った人の", "取扱説明書"], 150, WHITE, bold=2, gap=1.2)
    multiline(d, (W // 2, 2320),
              ["同僚・後輩・取引先", "——上司じゃない相手の守り方"],
              48, (206, 216, 232), gap=1.35)
    text(d, (W - 80, 2480), "智珠", 52, WHITE, anchor="rm", bold=1)
    img.convert("RGB").save(out, "JPEG", quality=88, optimize=True)


# ---------------- ch01 勾配マップ ----------------
def ch01(out):
    W, H = 1200, 780
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "相手を、勾配で見分ける", 42, NAVY, bold=1)
    # 縦（左・坂あり）
    rbox(d, [70, 140, 560, 680], WHITE, outline=DUSK, width=3)
    text(d, (315, 195), "縦の相手", 36, DUSK, bold=1)
    text(d, (315, 250), "評価・処遇・取引を握る", 24, INK)
    d.line([(140, 620), (490, 470)], fill=DUSK, width=8)  # 坂
    text(d, (315, 560), "上司・人事・決裁者・大口客", 23, INK)
    rbox(d, [110, 300, 520, 372], (247, 235, 230), radius=12)
    text(d, (315, 336), "守り＝受け流す（坂を転げない）", 24, DUSK, bold=1)
    # 横（右・平ら）
    rbox(d, [640, 140, 1130, 680], WHITE, outline=LEAF, width=3)
    text(d, (885, 195), "横の相手", 36, LEAF, bold=1)
    text(d, (885, 250), "評価を握っていない", 24, INK)
    d.line([(710, 545), (1060, 545)], fill=LEAF, width=8)  # 平ら
    text(d, (885, 590), "同僚・後輩・取引先・他部署", 23, INK)
    rbox(d, [680, 300, 1090, 372], (230, 242, 236), radius=12)
    text(d, (885, 336), "守り＝線を引く（正面から）", 24, LEAF, bold=1)
    rbox(d, [140, 706, 1060, 764], NAVY, radius=14)
    text(d, (W * .5, 735), "見るのは肩書きでなく「私の何を握っているか」の一点", 25, WHITE, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch03 お願い→基準への載せ替え ----------------
def ch03(out):
    W, H = 1200, 720
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "後輩は、お願いでなく“基準”で動かす", 42, NAVY, bold=1)
    rbox(d, [90, 150, 560, 560], WHITE, outline=DUSK, width=3)
    text(d, (325, 205), "お願い（人格）", 32, DUSK, bold=1)
    for i, s in enumerate(["「ちゃんとやって」", "「やる気ある?」", "→ 逆ギレ・被害者化"]):
        text(d, (325, 300 + i * 75), s, 25, INK if i < 2 else DUSK, bold=(i == 2))
    rbox(d, [640, 150, 1110, 560], WHITE, outline=LEAF, width=3)
    text(d, (875, 205), "事実と基準（仕事）", 32, LEAF, bold=1)
    for i, s in enumerate(["「締切は水曜正午」", "「品質基準はここ」", "→ 采配は上司へ返す"]):
        text(d, (875, 300 + i * 75), s, 25, INK if i < 2 else LEAF, bold=(i == 2))
    arrow_h(d, 566, 634, 355)
    text(d, (W * .5, 640), "私の好みでなく、締切と品質の話。動かすのは采配を持つ人へ", 25, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch04 範囲の可視化・エスカレの階段 ----------------
def ch04(out):
    W, H = 1200, 720
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "「お客様」は、無制限の免罪符ではない", 42, NAVY, bold=1)
    steps = [
        ("範囲を、可視化して返す", "契約・見積・仕様のどこまでが約束か"),
        ("個人で即答せず、持ち帰る", "「社として確認し、折り返します」"),
        ("記録を残し、担当を一人にしない", "口頭合意→メールで固める"),
        ("カスハラは会社が対処する問題", "安全配慮義務／一人で耐えない"),
    ]
    x0 = 150
    for i, (t, note) in enumerate(steps):
        y = 165 + i * 122
        rbox(d, [x0 + i * 60, y, x0 + i * 60 + 760, y + 96], NAVY if i == 3 else LIGHT,
             radius=14, outline=NAVY, width=2)
        c = WHITE if i == 3 else NAVY
        text(d, (x0 + i * 60 + 30, y + 34), f"{i+1}. {t}", 27, c, anchor="lm", bold=1)
        text(d, (x0 + i * 60 + 30, y + 70), note, 21, c if i == 3 else INK, anchor="lm")
    text(d, (W * .5, 690), "取引の坂は、個人でなく“会社ごと”で受ける", 24, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch05 私vs相手→共通の上位目的 ----------------
def ch05(out):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "他部署は、“共通の上位目的”で動かす", 42, NAVY, bold=1)
    # 上位目的（上・的）
    rbox(d, [430, 150, 770, 240], LEAF, radius=16)
    multiline(d, (600, 195), ["共通の上位目的", "（顧客・全体の締切）"], 26, WHITE, bold=1)
    # 私／相手（下・左右）
    rbox(d, [170, 430, 470, 540], LIGHT, radius=14, outline=NAVY, width=2)
    text(d, (320, 485), "私（依頼する側）", 26, NAVY, bold=1)
    rbox(d, [730, 430, 1030, 540], LIGHT, radius=14, outline=NAVY, width=2)
    text(d, (880, 485), "相手（他部署）", 26, NAVY, bold=1)
    # 対立の×
    d.line([(478, 485), (722, 485)], fill=DUSK, width=5)
    text(d, (600, 460), "私 対 あなた", 22, DUSK, bold=1)
    text(d, (600, 512), "だと動かない", 20, DUSK)
    # 上へ載せ替え矢印
    arrow_down(d, 320, 240, 424, color=LEAF)
    d.line([(320, 240), (320, 425)], fill=LEAF, width=6)
    arrow_down(d, 880, 240, 424, color=LEAF)
    d.line([(880, 240), (880, 425)], fill=LEAF, width=6)
    text(d, (W * .5, 620), "主語を「二人 対 案件」へ載せ替え、記録で固める", 25, NAVY, bold=1)
    img.save(out, "JPEG", quality=84, optimize=True)


# ---------------- ch02 同僚への守り ----------------
def ch02(out):
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "同僚——対等だから、正面から線を引く", 40, NAVY, bold=1)
    cards = [
        ("押し付け", "そらさず、等分へ戻す", "「ここからは各自のぶんで」"),
        ("手柄の横取り", "事前に、事実を記録で守る", "工程で切り分け＋送信済みメール"),
        ("陰口・詮索・NO", "加担せず、NOを普通の返事に", "「私はやめとくね」を軽く"),
    ]
    x0 = 70
    for i, (t, how, ex) in enumerate(cards):
        x = x0 + i * 375
        rbox(d, [x, 150, x + 340, 500], WHITE, outline=LEAF, width=3)
        rbox(d, [x, 150, x + 340, 222], LEAF, radius=18)
        text(d, (x + 170, 186), t, 28, WHITE, bold=1)
        multiline(d, (x + 170, 300), [how], 25, NAVY, bold=1)
        multiline(d, (x + 170, 400), _wrap2(ex), 22, INK, gap=1.25)
    rbox(d, [140, 540, 1060, 640], NAVY, radius=14)
    multiline(d, (W * .5, 590),
              ["毎日続く関係だから、焦土戦にしない。", "線は引く。ただし、勝ち負けにはしない。"],
              25, WHITE, bold=1, gap=1.3)
    img.save(out, "JPEG", quality=84, optimize=True)


def _wrap2(s):
    if len(s) <= 12:
        return [s]
    p = s.find("＋")
    if p > 0:
        return [s[:p + 1], s[p + 1:]]
    return [s[:len(s) // 2], s[len(s) // 2:]]


# ---------------- ch08 終章 勾配で守りを切り替える ----------------
def ch08(out):
    W, H = 1200, 740
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text(d, (W * .5, 58), "勾配で、守りを切り替える一枚", 42, NAVY, bold=1)
    # 中央の問い
    rbox(d, [390, 140, 810, 232], NAVY, radius=16)
    multiline(d, (600, 186), ["この相手は、私の評価を", "握っている？"], 27, WHITE, bold=1)
    # 分岐
    d.line([(600, 232), (600, 270)], fill=NAVY, width=6)
    d.line([(300, 270), (900, 270)], fill=NAVY, width=6)
    arrow_down(d, 300, 270, 330, color=DUSK)
    arrow_down(d, 900, 270, 330, color=LEAF)
    # 縦
    rbox(d, [110, 335, 500, 560], WHITE, outline=DUSK, width=3)
    text(d, (305, 385), "はい＝縦（上司）", 30, DUSK, bold=1)
    multiline(d, (305, 470),
              ["受け流す", "急所を踏まず、時間を持ち帰る"], 24, INK, gap=1.4)
    # 横
    rbox(d, [700, 335, 1090, 560], WHITE, outline=LEAF, width=3)
    text(d, (895, 385), "いいえ＝横（それ以外）", 27, LEAF, bold=1)
    multiline(d, (895, 470),
              ["線を引く", "対等を根拠に、正面から一本"], 24, INK, gap=1.4)
    rbox(d, [140, 600, 1060, 700], NAVY, radius=14)
    multiline(d, (W * .5, 650),
              ["明日へ渡す1枚＝①縦か横か　②握られているのは何か", "③今日引く線を、一本"],
              25, WHITE, bold=1, gap=1.3)
    img.save(out, "JPEG", quality=84, optimize=True)


GEN = {"ch01.jpg": ch01, "ch02.jpg": ch02, "ch03.jpg": ch03,
       "ch04.jpg": ch04, "ch05.jpg": ch05, "ch08.jpg": ch08}

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
