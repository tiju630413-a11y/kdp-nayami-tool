# 画像仕様書: 職場の理不尽から自分を守る台本36

- シリーズ: 今夜の処方箋 01 / 著者: 智珠
- カテゴリ: 職場・仕事 → 帯色 **ネイビー #1F3A5F**・アクセント **白**（cover/visual_system.md §2）
- 構成: 表紙プロンプト2本（本命＋予備）＋ 本文図解7点（ch01〜ch07 各1点）

---

## 運用手順（ユーザー向け）

1. 下の各プロンプトを Gemini に貼って生成（1点につき2〜4枚出して選ぶ）
2. 採用画像を `books/001_iikaesenai/images/` に保存（ファイル名は各項目の指定どおり）
3. 表紙: タイトル文字を「文字入れ指定」どおりに重ねる（Canva等。Gemini出力に文字が混入した場合はボツにして再生成）
4. 図解: 「ラベル表」の文字を各ノードに重ねる（後入れ。図の中の文字はすべてこの表が正）
5. 表紙のみ縮小視認テスト（下記）→ visual_system.md §4 の5項目を目視確認 → OKなら build へ
6. サイズ規定: 表紙 1600x2560 / JPEG品質80。図解は幅1200px以下 / JPEG品質80。EPUB合計 2〜3MB 目安

---

## 表紙

- ファイル名: `cover.jpg`（1600 x 2560 px、縦横比 1:1.6）
- キービジュアルの出典場面: 「はじめに」冒頭の**言い直しの夜**——帰りの電車で、暗い窓に映る自分を見ながら完璧な反論が遅れて届く場面（ch00_hajimeni.md 第4段落「帰りの電車は混んでいた。つり革につかまって、暗い窓に映る自分の顔を見ていたら…」）

### 本命プロンプト（夜の帰りの電車）

```
A flat vector illustration for a Japanese self-help book cover.
Scene: a tired office worker standing alone in a nearly empty commuter
train at night, holding a hanging strap, seen from behind, their faint
reflection visible in the dark train window, city lights blurred
outside the window
Mood: quiet, empathetic, slightly hopeful
Color scheme: muted tones harmonizing with deep navy #1F3A5F,
plenty of negative space in the upper and lower thirds
Composition: main subject in the center, simple background
Style: modern flat illustration, soft edges, no gradients overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

### 予備プロンプト（布団の中のスマホの光）

Geminiの本命出力が弱かったとき用。場面は同じく「はじめに」第6段落「布団の中で、検索窓に『上司 言い返せない』と打った指の感覚が…」から。

```
A flat vector illustration for a Japanese self-help book cover.
Scene: a person lying in bed under a blanket at night, looking at
a smartphone, the dark bedroom lit only by the soft glow of the
phone screen on their face
Mood: quiet, empathetic, slightly hopeful
Color scheme: muted tones harmonizing with deep navy #1F3A5F,
plenty of negative space in the upper and lower thirds
Composition: main subject in the center, simple background
Style: modern flat illustration, soft edges, no gradients overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

### 文字入れ指定（Canva等で後入れ。visual_system.md §1 グリッド準拠）

- **上部 12%（シリーズ帯）**: 「今夜の処方箋 01」（番号は2桁ゼロ埋め）。白文字、細めのゴシック、小さめ・センター寄せ
- **中央 55%**: キービジュアル（文字は一切載せない）
- **タイトル帯 25%**: **単色ベタ #1F3A5F**。白文字・太ゴシック系（例: 源ノ角ゴシック Heavy / Noto Sans JP Black）で2行:
  - 1行目: 「職場の理不尽から」（8字 ≤ 13字/行 OK）
  - 2行目: 「自分を守る台本36」（9字 ≤ 13字/行 OK。「36」は等幅で大きめに強調可）
  - サブタイトル1行（タイトルの下、小さめの白文字）: 「言い返せなくていい。「守りの一言」だけ持っていく」
- **下部 8%**: 著者名「智珠」右寄せ・白
- 縮小視認テスト: `python3 -c "from PIL import Image; Image.open('books/001_iikaesenai/images/cover.jpg').resize((90,144)).save('books/001_iikaesenai/images/thumb_test.png')"`
  → visual_system.md §4 の5項目（タイトル可読 / 悩みが1秒で分かる / 帯色一致 / 埋没しない / シリーズ統一感）を目視確認

---

## 本文図解（各章1点・計7点）

図解共通: 横4:3、幅1200px以下、ラベル文字はすべて後入れ。挿入時は EPUB 側で図の直前後に1行空ける。

### 第1章: 言い返せないのは、装備の問題だ

- ファイル名: `ch01.jpg`
- 挿入位置: ch01.md 見出し「### 「守りの一言」の三つの条件」の節内。箇条書き3行（「- ① 同意しない——」「- ② 反撃しない——」「- ③ 時間を稼ぐ——」）の直後、「相手を変える言葉ではない。」で始まる段落の直前
- 系統: **構造図**（守りの一言の3条件。中心1ノード＋周囲3ノード、矢印なし・接続線3本）
- 図解対象の理由: 本書全体の核となる定義で、「守りの一言＝おとなしい謝罪」と誤読されやすい。3条件が同時に成立する構造を1枚で固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing one central rounded square (a shield-like emblem) surrounded
by exactly three rounded rectangular nodes arranged in a triangle
around it (one on top, two below), each of the three nodes connected
to the center by a single short straight line, no arrows, no loop
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 中心ノード＝「守りの一言」
  - 上ノード＝「① 同意しない」（補足小文字: 事実でない非を認めない）
  - 左下ノード＝「② 反撃しない」（補足: 相手の優位をその場では脅かさない）
  - 右下ノード＝「③ 時間を稼ぐ」（補足: 決着をあとへ持ち越す）
- 代替テキスト: 守りの一言は「同意しない・反撃しない・時間を稼ぐ」の3条件をすべて同時に満たす短い言葉である、という定義を示す図。

### 第2章: 会議で頭ごなしに否定されたら

- ファイル名: `ch02.jpg`
- 挿入位置: ch02.md 章導入の最終段落（「もうひとつ、この章の前提を置いておく。」で始まり「…持ち帰るのは勝利ではなく、あなたの品位と情報だ。」で終わる段落）の直後、見出し「### D01 データごと否定された…」の直前
- 系統: **対処フロー**（直線4ノード、左→右の矢印3本、ループなし）
- 図解対象の理由: この章で最も誤読されやすいのは「その場で反論も証明もしない＝負け」という読み。検証を観客のいない時間へ動かす一連の流れとして描き直す
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a straight horizontal flow of exactly four rounded rectangular
nodes connected left to right by exactly three arrows all pointing
right, a straight linear sequence, no loop, no branches; the first
node slightly darker, the last node slightly brighter
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - ノード1＝「会議で頭ごなしの否定」（補足: 観客が最多＝儀式の土俵）
  - ノード2＝「守りの一言で受ける」（補足: 同意せず・反撃せず）
  - ノード3＝「検証を会議のあとへ」（補足: 土俵を後ろへずらす）
  - ノード4＝「観客のいない場で事実を示す」（補足: 準備の勝負に変わる）
- 代替テキスト: 会議で否定されたら、その場で証明せず、守りの一言で受けて検証を会議後へ移し、観客のいない場で事実を示す——という4段階の流れを示す図。

### 第3章: みんなの前で嫌味を言われたら

- ファイル名: `ch03.jpg`
- 挿入位置: ch03.md 章導入の段落「だからこの章の7本は、切れ味を持たせていない。使うのは三つの系統だけだ。」の直後、見出し「### D09 「もう終わったの？ 暇なんだね」型の当てこすり」の直前
- 系統: **構造図**（分類ツリー。上1ノード→下3ノード、下向き矢印3本）
- 図解対象の理由: 7本の台本が3系統（気づかないふり/受け流し/事実化）に分かれる章の設計が文章だけだと読み飛ばされやすく、どの台本がどの系統か迷子になる
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a tree diagram: exactly one rounded rectangular node centered
at the top, branching down to exactly three rounded rectangular nodes
in a row below it, connected by exactly three arrows pointing downward,
no loop, no further levels
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 上ノード＝「人前の嫌味」（補足: 音量を絞った儀式）
  - 下左ノード＝「気づかないふり」（補足: D09・D11／業務の部分にだけ返事）
  - 下中ノード＝「受け流し」（補足: D10・D12・D13／栄養だけ受け取り皿を戻す）
  - 下右ノード＝「事実化」（補足: D14・D15／評価でなく事実として受領）
- 代替テキスト: 人前の嫌味への返しは「気づかないふり（D09・D11）」「受け流し（D10・D12・D13）」「事実化（D14・D15）」の3系統に分かれる、という章の全体地図。

### 第4章: 無理な仕事を押しつけられそうなとき

- ファイル名: `ch04.jpg`
- 挿入位置: ch04.md 章導入の段落「先に、この章の設計を明かしておく。」で始まり「…この章では③時間を稼ぐが主役になる。」で終わる段落の直後、次段落「もう一つ。あなたは職場で「いい人の椅子」に…」の直前
- 系統: **Before→After（左右対比）**（左3ノード・右3ノード、各列とも下向き矢印2本）
- 図解対象の理由: 「断る勇気の話」と誤読されやすい章。押しつけの燃料は即答であり、返事を後ろへずらすだけで成立が崩れる、という対比を固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a before-and-after comparison split into left and right halves
by a thin vertical divider line: on the left, a vertical column of
exactly three rounded rectangular nodes in muted gray tones connected
by exactly two downward arrows; on the right, a vertical column of
exactly three rounded rectangular nodes in navy and white tones
connected by exactly two downward arrows; the two columns are parallel
and not connected to each other, no loop
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F
plus neutral gray for the left half, white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 左列見出し＝「Before: 即答」
  - 左1＝「金曜17時『今日中にできるよね？』」 / 左2＝「即答『はい』」 / 左3＝「押しつけ成立（週末が消える）」
  - 右列見出し＝「After: 保留」
  - 右1＝「金曜17時『今日中にできるよね？』」 / 右2＝「『量を見て判断したいので10分ください』」 / 右3＝「量を測って条件の話へ（段取りの土俵）」
- 代替テキスト: 同じ「今日中にできるよね？」でも、即答すれば押しつけが成立し、10分の保留を挟めば段取りの交渉に変わる、という対比を示す図。

### 第5章: 謝らされ続ける・詰められるとき

- ファイル名: `ch05.jpg`
- 挿入位置: ch05.md 見出し「### D26 自分のせいでないことへの謝罪を求められる」の節内。段落「謝罪にはふたつの層がある。」で始まり「…あなたを守る線になる。」で終わる段落の直後、次段落「言葉の在庫をいくつか持っておくと…」の直前
- 系統: **構造図**（2層の分解。左に上下2段の積み層、右に受け先2ノード、右向き矢印2本）
- 図解対象の理由: 部分謝罪の「気持ちには応じ、事実は認めない」は、文章だけだと「結局謝るのか謝らないのか」と混同されやすい。謝罪を2層に分解し、行き先が別であることを図で固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing on the left side one tall rounded rectangle divided
horizontally into exactly two stacked layers (top layer lighter,
bottom layer darker), and on the right side exactly two separate
rounded rectangular nodes placed one above the other; exactly two
arrows pointing right: one from the top layer to the upper right
node, one from the bottom layer to the lower right node, no loop,
no other connections
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 左ブロック見出し＝「謝罪のふたつの層」
  - 左上層＝「感情の層」（補足: 相手の気持ちに応える）
  - 左下層＝「事実の層」（補足: 非を認めるかどうか）
  - 右上ノード＝「短く応じる『ご心配をおかけした点は、申し訳ないと思っています』」
  - 右下ノード＝「経緯の確認に預ける『経緯は整理して、改めてご報告します』」
- 代替テキスト: 謝罪は「感情の層」と「事実の層」に分けられ、部分謝罪は感情の層にだけ短く応じ、事実の層は経緯の確認に預ける——全面降伏との違いを示す図。

### 第6章: 一対一の密室で

- ファイル名: `ch06.jpg`
- 挿入位置: ch06.md 章導入の段落「怖がらせるために書いているのではない。装備を一段増やしてもらうために書いている。」で始まり「…この二つを必ず編み込んである。」で終わる段落の直後、見出し「### D31 会議室に呼ばれて長時間の説教が始まった」の直前
- 系統: **構造図**（「5行のメモ」のカード図。1枚のメモカード＋横罫5行、矢印なし）
- 図解対象の理由: 本章と終章の防具の中核「5行のメモ」の5項目は、本文中で一度しか列挙されず、以降は「例の5行のメモ」と参照される。1枚で参照先を固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a single large smartphone-memo-style card (rounded rectangle
with a slightly darker header bar at the top) containing exactly five
horizontal blank line fields stacked vertically inside it, each field
drawn as a thin rounded bar with a small dot marker on its left,
no arrows, nothing else around the card
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - ヘッダー＝「5行のメモ（その日のうちに）」
  - 行1＝「日時と場所」
  - 行2＝「相手の名前」
  - 行3＝「言われた言葉」
  - 行4＝「自分が返した言葉」
  - 行5＝「体に起きたこと」
- 代替テキスト: 密室のやり取りはその日のうちに「日時と場所・相手の名前・言われた言葉・自分が返した言葉・体に起きたこと」の5行でメモに残す、という記録の型を示す図。

### 終章: 台本が効かない相手からは、逃げていい

- ファイル名: `ch07.jpg`
- 挿入位置: ch07.md 見出し「### 明日の自分に持たせる3枚のカード」の節内。段落「三枚目は、自分との約束だ。」で始まり「…カードはさらに強くなる。」で終わる段落の直後、次段落「書き終えたら、そのメモを画面の目立つ場所に置く。」の直前
- 系統: **構造図**（3枚のカード図。横並び3ノード、矢印なし）
  - 注: 指示書の選択肢「効かない相手のサイン3つ」は draft では**サインが4つ**（頻度・人格化・密室化・体のサイン）のため不採用。原稿と点数が一致する「3枚のカード」を採用した
- 図解対象の理由: 本書の締めのワーク。「36本全部を覚える本」と誤読されやすいのに対し、持ち歩く装備は3枚だけ、という結論を1枚に固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing exactly three card-shaped rounded rectangles of the same size
arranged side by side in a horizontal row, slightly fanned like cards
held in a hand, each card with a small simple icon area at the top
(a speech bubble shape, a second speech bubble shape, a small heart
shape) and a blank body area below, no arrows, no other elements
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 図タイトル＝「明日の自分に持たせる3枚のカード」
  - カード1＝「守りの一言」（補足: 36本から、あの人用に1本だけ）
  - カード2＝「二の手」（補足: 食い下がられたときの二手目）
  - カード3＝「自分との約束」（補足: サインが3つ揃ったら記録を持って相談する）
- 代替テキスト: 明日持ち歩く装備は「守りの一言1本・その二の手・相談に行く自分との約束」の3枚だけでよい、という終章のワークの中身を示す図。

---

## ファイルサイズ試算

表紙1点＋図解7点 × JPEG品質80（図解は白背景フラットで軽い）＝ 合計1.5〜2MB 想定。EPUB 3MB 目安内。点数追加はしない。

---

## 自己チェック（prompts/06_images.md §4）

- [x] 全プロンプト（表紙2本＋図解7本）に `no text, no letters, no numbers` 系のネガティブ指定がある
- [x] 帯色 #1F3A5F はカテゴリ「職場・仕事」のパレット（visual_system.md §2）と一致。アクセントは白
- [x] 挿入位置はすべて draft の実在の見出し・段落を「見出し名＋段落冒頭の文言」で特定している（各章で照合済み）
- [x] 代替テキストはすべて「図が伝える内容」（定義・流れ・対比・型）で書き、「〜のイラスト」型の画像説明にしていない
- [x] 点数は各章1点×7＋表紙で過剰でない。白背景フラット図解主体で EPUB 3MB 目安内
