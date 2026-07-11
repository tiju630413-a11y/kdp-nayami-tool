# 3冊目『言い返せなかった夜の心の片付け方』Gemini生成プロンプト集（表紙）

各プロンプトをGeminiに貼って生成（1点につき2〜4枚出して選ぶ）→ 採用画像を
`books/003_yoru_kaifuku/images/src/` に指定ファイル名（.png）で保存 → 送っていただければ私が合成します。
※すべて「文字なし」で生成されます。タイトル・サブタイトル・著者名は私が後から重ねます。
※本命が弱ければ予備を使ってください。01/02と同じネイビー #1F3A5F 基調・縦横比5:8。

---

## シリーズとの差別化メモ（なぜこの絵か）
- 01＝夜の帰りの電車（戦場からの帰り道）、02＝夜のオフィス＋五つの扉（相手）。
- 03＝**帰宅後・夜の自室**。回復編なので、01予備（布団＋スマホの光＝苦痛）とは逆に、
  **ベッドサイドの灯り＝自分を手当てする温かさ**を一点だけ差す。ネイビーの夜に、
  ひとつだけ灯る琥珀色の光が「回復」のモチーフ。三部作の締めにふさわしい静けさ。

---

## 本命プロンプト（夜の自室・ベッドサイドの灯りに、ひとり静かに座る）
**保存ファイル名: `src/cover_main.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a person sitting quietly on the edge of a bed in a dark bedroom
late at night, seen from behind or in soft side view, a small bedside
table lamp beside them casting a gentle warm glow into the dim room, a
closed notebook resting on the nightstand; the mood is one of quietly
tending to oneself after a long day, calm rather than distressed
Mood: quiet, calm, tender, gently hopeful, soothing
Color scheme: muted tones harmonizing with deep navy #1F3A5F for the
night room, with a single soft warm amber glow from the bedside lamp as
the only accent; plenty of negative space in the upper and lower thirds
Composition: the seated figure and the lamp slightly off-center, the
warm glow pooling softly around them, simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

## 予備プロンプト（灯りのついた無人のベッドサイド＝一日を置いて眠る支度）
**保存ファイル名: `src/cover_spare.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a dark quiet bedroom at night seen from a gentle angle, a neatly
made bed with a small bedside table lamp switched on, casting a soft
warm circle of light over the pillow and a closed notebook on the
nightstand; no phone, the room peaceful and still, as if the day has
been set down and the room is prepared for rest
Mood: quiet, calm, tender, gently hopeful, soothing
Color scheme: muted tones harmonizing with deep navy #1F3A5F for the
night room, with a single soft warm amber glow from the bedside lamp as
the only accent; plenty of negative space in the upper and lower thirds
Composition: the lamp and nightstand slightly off-center, the warm glow
pooling softly over the bed, simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

---

## 保存後にやること
1. 採用画像を `src/cover_main.png`（または `src/cover_spare.png`）として保存し、送ってください。
2. 私が `compose_labels.py` でタイトル帯（今夜の処方箋 03／タイトル2行／サブタイトル／智珠）を重ね、
   `cover.jpg`（1600×2560）に合成 → EPUBを再ビルドします。
3. 縮小視認テスト（サムネイルでタイトルが読めるか）を確認してから確定します。
※Gemini出力に文字が混入したら、その一枚はボツにして再生成してください（文字は必ず私が後入れします）。
```
