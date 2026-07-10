# 6冊目『中間管理職の身の守り方』Gemini生成プロンプト集（表紙）

各プロンプトをGeminiに貼って生成（1点につき2〜4枚出して選ぶ）→ 採用画像を
`books/006_itabasami/images/src/` に指定ファイル名（.png）で保存 → 送っていただければ私が合成します。
※すべて「文字なし」で生成されます。タイトル・サブタイトル・著者名は私が後から重ねます。
※01〜05と同じネイビー #1F3A5F 基調・縦横比5:8。

---

## シリーズとの差別化メモ（なぜこの絵か）
- 01=夜の電車、02=夜のオフィス＋五つの扉、03=夜の自室、04=同じ目線の横の相手、05=外へ歩き出す後ろ姿。
- 06は「板挟み（縦の上下）」。だから絵の核は、**上と下の両方から押されても、潰れずにまっすぐ立つ一人**。
  上から降りてくる重さ（無理・数字）と、下から突き上げる圧を、片手ずつで受け止めながら、
  自分の足場を保って立っている。折れそうで折れない、静かな踏ん張り。負け姿ではなく、**耐えて立つ品位**。
  一点だけ差す暖色の光＝その人の足元（守られている自分）。ネイビーの夜に、立ち姿がひとつ浮かぶ。

---

## 本命プロンプト（上下の重みに挟まれても、潰れず立つ人物）
**保存ファイル名: `src/cover_main.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a single office worker standing upright in the center, viewed
from the front or slightly side-on, calmly holding their ground while
being pressed from two directions at once — a heavy weight or downward
pressure bearing down from above, and an upward push rising from below;
the figure does not buckle, standing straight and composed on a firm
footing, quietly enduring the squeeze from both sides
Mood: quiet resilience, composure under pressure, dignified endurance —
strained but not broken; calm rather than dramatic
Color scheme: muted tones harmonizing with deep navy #1F3A5F for the
pressures above and below, with a single soft warm light at the
figure's feet as the only accent; plenty of negative space in the
upper and lower thirds
Composition: the standing figure centered, the pressure from above and
the pressure from below rendered simply and abstractly (arrows, blocks,
or gradients of weight), simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

## 予備プロンプト（上下の矢印に挟まれた中央の人物・より抽象的に）
**保存ファイル名: `src/cover_spare.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a lone figure standing calmly at the center of the frame,
positioned between a large downward-pointing pressure from the top of
the composition and an upward-pointing pressure from the bottom; the
person keeps their balance and posture, neither crushed nor toppled,
holding a small steady space of their own in the middle
Mood: quiet, composed, resilient — a still point held between two
opposing forces
Color scheme: muted tones harmonizing with deep navy #1F3A5F for the
opposing pressures, with one soft warm accent light around the central
figure; generous negative space top and bottom
Composition: strong vertical symmetry, the figure as a calm still point
in the middle, the two opposing forces abstract and simple
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

---

## 保存後にやること
1. 採用画像を `src/cover_main.png`（または `cover_spare.png`）として保存し、送ってください。
2. 私が `compose_labels.py` でタイトル帯（今夜の処方箋 06／中間管理職の／身の守り方／サブ／智珠）を重ね、
   `cover.jpg`（1600×2560）に合成 → EPUBを再ビルドします。
3. 縮小視認テスト（サムネイルでタイトルが読めるか）を確認してから確定します。
※Gemini出力に文字が混入したら、その一枚はボツにして再生成してください（文字は必ず私が後入れします）。
※現在は文字なしベースが未着のため、Pillowフォールバックの表紙（上下矢印＋立つ人物）を仮生成済みです。
```