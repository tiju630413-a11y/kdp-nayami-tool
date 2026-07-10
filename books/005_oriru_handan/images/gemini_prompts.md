# 5冊目『職場の降り方』Gemini生成プロンプト集（表紙）

各プロンプトをGeminiに貼って生成（1点につき2〜4枚出して選ぶ）→ 採用画像を
`books/005_oriru_handan/images/src/` に指定ファイル名（.png）で保存 → 送っていただければ私が合成します。
※すべて「文字なし」で生成されます。タイトル・サブタイトル・著者名は私が後から重ねます。
※本命が弱ければ予備を使ってください。01〜04と同じネイビー #1F3A5F 基調・縦横比5:8。

---

## シリーズとの差別化メモ（なぜこの絵か）
- 01=夜の電車、02=夜のオフィス＋五つの扉、03=夜の自室（ベッドサイド）、04=同じ目線に並ぶ横の相手。
- 05は「出口（降りる）」。だから絵の核は、**削られる場所から、外へ一歩踏み出す後ろ姿**。
  暗く冷たいオフィスを背に、前方の“外の光”へ向かう。負けや逃避でなく、**安堵と解放**のトーン。
  一点だけ差す暖色の光＝次の場所。ネイビーの夜に、出口の光がひとつ灯る。

---

## 本命プロンプト（夜、オフィスの扉から外の光へ歩き出す後ろ姿）
**保存ファイル名: `src/cover_main.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a lone office worker seen from behind, walking out through the
open doorway of a dark office building at night, stepping toward a
softer, warmer light outside; behind them the office is dim and cold,
ahead of them the exit opens onto calmer open space; a quiet sense of
leaving — not defeat, but relief
Mood: quiet, calm, a little hopeful, unburdened
Color scheme: muted tones harmonizing with deep navy #1F3A5F for the
office behind, with a soft warm light at the doorway ahead as the only
accent; plenty of negative space in the upper and lower thirds
Composition: the figure slightly off-center, walking away from the
viewer toward the lit doorway, simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

## 予備プロンプト（夜、外階段を降りて街の灯りへ向かう後ろ姿）
**保存ファイル名: `src/cover_spare.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a lone office worker seen from behind, quietly walking down an
outdoor staircase away from a lit office building at night, descending
toward a calm street below where a few warm lights glow; the building
they are leaving recedes above and behind them
Mood: quiet, calm, a little hopeful, unburdened
Color scheme: muted tones harmonizing with deep navy #1F3A5F, with a
few soft warm lights below as the only accent; plenty of negative space
in the upper and lower thirds
Composition: the figure on the stairs slightly off-center, descending
toward the lower foreground, simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

---

## 保存後にやること
1. 採用画像を `src/cover_main.png`（または `cover_spare.png`）として保存し、送ってください。
2. 私が `compose_labels.py` でタイトル帯（今夜の処方箋 05／タイトル2行／サブ／智珠）を重ね、
   `cover.jpg`（1600×2560）に合成 → EPUBを再ビルドします。
3. 縮小視認テスト（サムネイルでタイトルが読めるか）を確認してから確定します。
※Gemini出力に文字が混入したら、その一枚はボツにして再生成してください（文字は必ず私が後入れします）。
