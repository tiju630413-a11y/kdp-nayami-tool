# 4冊目『職場の困った人の取扱説明書』Gemini生成プロンプト集（表紙）

各プロンプトをGeminiに貼って生成（1点につき2〜4枚出して選ぶ）→ 採用画像を
`books/004_yoko_rifujin/images/src/` に指定ファイル名（.png）で保存 → 送っていただければ私が合成します。
※すべて「文字なし」で生成されます。タイトル・サブタイトル・著者名は私が後から重ねます。
※本命が弱ければ予備を使ってください。01/02と同じネイビー #1F3A5F 基調・縦横比5:8。

---

## シリーズとの差別化メモ（なぜこの絵か）
- 02『苦手な上司の取扱説明書』＝夜のオフィスに一人＋五つの扉（上司＝見上げる相手・型）。
- 04は「上司以外＝勾配のない“横”の相手」。だから絵の核は、**全員が同じ目線の高さに並ぶ**こと。
  誰も上から見下ろさず、誰も下にいない。対等＝坂がない、を一枚で伝える。02の“取扱説明書”棚に並べつつ、
  「見上げる02／同じ目線の04」で内容の違いが絵でわかる。

---

## 本命プロンプト（同じ目線に並ぶ数人と向き合う）
**保存ファイル名: `src/cover_main.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a lone office worker standing calmly in a quiet office at night,
facing a row of three or four other people who all stand at exactly the
same eye level as them — no one towering above, no one below; each of the
others is a slightly different simple silhouette, suggesting a colleague,
a junior, and an outside client; a faint horizontal line runs along the
floor beneath everyone, quietly emphasizing that they all stand on the
same level
Mood: quiet, composed, quietly empowering, a little tense
Color scheme: muted tones harmonizing with deep navy #1F3A5F,
plenty of negative space in the upper and lower thirds
Composition: the main figure slightly to one side, the row of others
facing them at equal height, simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

## 予備プロンプト（夜のデスク島・同じ平面に座る同僚たち）
**保存ファイル名: `src/cover_spare.png`**
```
A flat vector illustration for a Japanese self-help book cover.
Scene: a quiet office island of desks at night, with several coworkers
seated around it, all on one flat level, none raised above the others;
in the foreground, the reader's own empty chair is seen from behind, as
if they have just stood up; only a few desk lamps are lit, the rest of
the room in soft shadow
Mood: quiet, composed, quietly empowering
Color scheme: muted tones harmonizing with deep navy #1F3A5F,
plenty of negative space in the upper and lower thirds
Composition: the desk island roughly centered, coworkers evenly around
it at equal height, simple flat background
Style: modern flat illustration, soft edges, no gradient overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

---

## 保存後にやること
1. 採用画像を `src/cover_main.png`（または `cover_spare.png`）として保存し、送ってください。
2. 私が `compose_labels.py` でタイトル帯（今夜の処方箋 04／タイトル2行／サブ／智珠）を重ね、
   `cover.jpg`（1600×2560）に合成 → EPUBを再ビルドします。
3. 縮小視認テスト（サムネイルでタイトルが読めるか）を確認してから確定します。
※Gemini出力に文字が混入したら、その一枚はボツにして再生成してください（文字は必ず私が後入れします）。
