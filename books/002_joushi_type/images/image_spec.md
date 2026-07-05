# 画像仕様書: 苦手な上司の取扱説明書

- シリーズ: 今夜の処方箋 **02** / 著者: 智珠
- カテゴリ: 職場・仕事 → 帯色 **ネイビー #1F3A5F**・アクセント **白**（cover/visual_system.md §2。1冊目と同色＝シリーズ棚の統一）
- 構成: 表紙プロンプト2本（本命＋予備）＋ 本文図解7点（ch01〜ch07 各1点）
- 姉妹書との関係: 1冊目『職場の理不尽から自分を守る台本36』と**同じ共通レイアウト・同じ帯色**で「同じシリーズの別の1冊」と分かるようにし、**キービジュアルだけ差し替える**（1冊目＝夜の帰りの電車 → 本書＝夜のオフィス／五つの扉）。

---

## 運用手順（ユーザー向け）

1. 下の各プロンプトを Gemini に貼って生成（1点につき2〜4枚出して選ぶ）
2. 採用画像を `books/002_joushi_type/images/` に保存（ファイル名は各項目の指定どおり）
3. 表紙: タイトル文字を「文字入れ指定」どおりに重ねる（Canva等。Gemini出力に文字が混入した場合はボツにして再生成）。**1冊目 cover.jpg とグリッド・帯色・フォントを完全にそろえる**
4. 図解: 「ラベル表」の文字を各ノードに重ねる（後入れ。図の中の文字はすべてこの表が正）
5. 表紙のみ縮小視認テスト（下記）→ visual_system.md §4 の5項目を目視確認 → **1冊目 cover と並べて「同じシリーズ」と分かるか**も確認 → OKなら build へ
6. サイズ規定: 表紙 1600x2560 / JPEG品質80。図解は幅1200px以下 / JPEG品質80。EPUB合計 2〜3MB 目安

---

## 表紙

- ファイル名: `cover.jpg`（1600 x 2560 px、縦横比 1:1.6）
- キービジュアルの狙い: 「困った上司の下で働く人／五つのタイプの気配」を象徴する、夜〜室内の情景。1冊目の**夜の帰りの電車**とはモチーフを変え、本書は**夜のオフィスに一人残る後ろ姿**を主役にする。背景に、形の少しずつ違う**五つの閉じた扉（＝五型の気配）**を沈めておく。

### 本命プロンプト（夜のオフィスに一人残る後ろ姿＋五つの扉）

```
A flat vector illustration for a Japanese self-help book cover.
Scene: a lone office worker seen from behind, sitting at a desk in an
otherwise empty office late at night, only a small desk lamp lit; in
the dim background wall there are exactly five closed doors of slightly
different shapes and sizes, each faintly suggesting a different unseen
presence, arranged in a quiet row
Mood: quiet, empathetic, slightly hopeful, a little tense
Color scheme: muted tones harmonizing with deep navy #1F3A5F,
plenty of negative space in the upper and lower thirds
Composition: the seated figure in the center, the five doors softened
into the shadowed background, simple flat background
Style: modern flat illustration, soft edges, no gradients overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

### 予備プロンプト（夜の廊下で五つの扉に向き合う後ろ姿）

Geminiの本命出力が弱かったとき用。場面違いで、五型の気配をより前面に出す。

```
A flat vector illustration for a Japanese self-help book cover.
Scene: a person standing alone from behind in a dim office corridor at
night, facing exactly five closed doors lined up along the wall, each
door a slightly different shape and casting a slightly different shadow,
the whole hallway lit only by faint ceiling light
Mood: quiet, empathetic, slightly hopeful, a little tense
Color scheme: muted tones harmonizing with deep navy #1F3A5F,
plenty of negative space in the upper and lower thirds
Composition: the standing figure in the center foreground, the five
doors receding down the corridor, simple flat background
Style: modern flat illustration, soft edges, no gradients overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

### 文字入れ指定（Canva等で後入れ。visual_system.md §1 グリッド準拠。1冊目と同一設定）

- **上部 12%（シリーズ帯）**: 「今夜の処方箋 02」（番号は2桁ゼロ埋め）。白文字、細めのゴシック、小さめ・センター寄せ。1冊目「今夜の処方箋 01」と同じ位置・同じ級数
- **中央 55%**: キービジュアル（文字は一切載せない）
- **タイトル帯 25%**: **単色ベタ #1F3A5F**。白文字・太ゴシック系（例: 源ノ角ゴシック Heavy / Noto Sans JP Black）で2行。メインタイトル『苦手な上司の取扱説明書』を **13字/行以内**で行割りする:
  - 1行目: 「苦手な上司の」（6字 ≤ 13字/行 OK）
  - 2行目: 「取扱説明書」（5字 ≤ 13字/行 OK。字間を広めに取り、行頭を1行目とそろえる）
  - サブタイトル（タイトルの下、小さめの白文字）: 「あなたの上司は5つの型のどれか。/型が分かれば、急所が分かる。」（長いので2行に折る。「型が分かれば、急所が分かる。」を軽く強調可）
- **下部 8%**: 著者名「智珠」右寄せ・白（1冊目と同位置）
- 縮小視認テスト: `python3 -c "from PIL import Image; Image.open('books/002_joushi_type/images/cover.jpg').resize((90,144)).save('books/002_joushi_type/images/thumb_test.png')"`
  → visual_system.md §4 の5項目（タイトル可読 / 悩みが1秒で分かる / 帯色一致 / 埋没しない / シリーズ統一感）を目視確認。特に**5項目め**は、1冊目 cover.jpg と横に並べて「同じ著者の別の1冊」に見えるかで判定する

---

## 本文図解（各章1点・計7点）

図解共通: 横4:3、幅1200px以下、ラベル文字はすべて後入れ。挿入時は EPUB 側で図の直前後に1行空ける。

### 第1章 なぜ“型”で見るのか——地図と急所【看板図＝上司の5型マップ】

- ファイル名: `ch01.jpg`
- 挿入位置: ch01.md 見出し「### 「型の急所」とは何か」の節内。段落「五つの型と、その急所を、先に並べておく。……ここでは地図として、全体の見取り図だけ持ってほしい。」の直後、箇条書きの一行目「- **高圧型（怒鳴る人）**——急所は、軽く扱われることへの恐れだ。」の直前
- 系統: **構造図（放射マップ）**。中心1ノード＋放射状に5ノード、中心と各ノードを**単線5本**でつなぐ（矢印なし・ループなし）。5ノードはそれぞれ上下2段に割った札で、上段＝型名、下段＝急所を入れる想定
- 図解対象の理由: 本書の背骨「上司の5型」と「型の急所」を一枚で固定する**看板図**。文章だと五つの型と五つの急所の対応が読み飛ばされ、どの型がどの恐れかを取り違えやすい。以降の全章がこの地図を参照する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing one central rounded emblem (a small map or compass shape) with
exactly five rounded rectangular cards arranged radially around it (like
five spokes of a wheel), each card connected to the center by a single
straight line, no arrows, no loop; each of the five cards is divided
horizontally into two stacked zones (an upper zone and a lower zone)
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 中心ノード＝「上司の5型」
  - カード1 上段＝「高圧型（怒鳴る人）」／下段＝急所「軽く扱われる不安」
  - カード2 上段＝「論破型（正論で詰める人）」／下段＝急所「間違いを認める恐れ」
  - カード3 上段＝「マウント型（張り合う人）」／下段＝急所「価値がない恐れ」
  - カード4 上段＝「被害者型（不機嫌で支配する人）」／下段＝急所「無視される恐れ」
  - カード5 上段＝「搾取型（押し付ける人）」／下段＝急所「断られる前例ができる恐れ」
- 代替テキスト: 困った上司は「高圧・論破・マウント・被害者・搾取」の5つの型に分けられ、各型にはそれぞれ「軽く扱われる／間違いを認める／価値がない／無視される／前例ができる」という別々の急所（裏の恐れ）が対応する、という本書全体の地図。

### 第2章 高圧型——怒鳴る人（儀式を成立させない）

- ファイル名: `ch02.jpg`
- 挿入位置: ch02.md 見出し「### 全面降伏が、いちばん高くつく」の節内。段落「Afterは、動作を一つ変えるだけだ。……積み上がると眠りの深さまで変えていく。」の直後、次段落「ここで一つ、下ろしておきたい荷物がある。」の直前
- 系統: **Before→After（左右対比）**。左3ノード・右3ノード、各列とも下向き矢印2本、中央に細い縦の仕切り線。二列は互いにつながない（ループなし）
- 図解対象の理由: この章で最も誤読されやすいのは「謝る量が足りなかった」という読み。問題は量ではなく、**即座の全面降伏そのものが儀式を100%成立させている**点にある。同じ怒鳴りを、燃料を渡す受け方／渡さない受け方で対比して固定する
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
  - 左列見出し＝「Before: 全面降伏」
  - 左1＝「人前で怒鳴られる」 / 左2＝「即座に『すみません』を連呼」 / 左3＝「儀式が100%成立（次もあなたが選ばれる）」
  - 右列見出し＝「After: 記録の手」
  - 右1＝「人前で怒鳴られる」 / 右2＝「メモを取りつつ『事実関係だけ確認させてください』」 / 右3＝「手応えを渡さない（足が遠のく）」
- 代替テキスト: 同じ怒鳴りでも、即座の全面降伏は儀式を成立させて次も自分が標的になり、謝罪語を足さず記録の手で受ければ相手に手応えが渡らず儀式が空振りになる、という受け方の対比。

### 第3章 論破型——正論で詰める人（勲章は渡し、決定は残す）

- ファイル名: `ch03.jpg`
- 挿入位置: ch03.md 段落「そのために使うのが、論点を二つに割る技術だ。……」から始まる説明群のあと、段落「……次の三本は、この「割って、渡して、残す」を、場面ごとに形にした守りの一言だ。」の直後、見出し「### 守りの一言① 原因の追及を、未来へ動かす」の直前
- 系統: **構造図（分岐）**。上1ノード（議論）から下2ノードへ**下向き矢印2本**で枝分かれ。左右のノードの先に、行き先を示す小さなマーカーを各1個（左＝相手／右＝自分）。ループなし
- 図解対象の理由: この章の核「論点を二つに割る」は、文章だと「結局、正しさで負けを認めるのか」と混同されやすい。**〈何が正しいか〉は相手へ丸ごと渡し、〈どう決めるか〉だけ手元に残す**という分割を、一枚で固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing one rounded rectangular node at the top branching down into
exactly two rounded rectangular nodes below (left and right), connected
by exactly two arrows pointing downward; to the left of the left node a
small outward arrow marker, to the right of the right node a small
marker pointing back inward; a single branch level only, no loop
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
the left node lighter, the right node in solid navy, white background,
clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 上ノード＝「詰め・指摘（議論）」
  - 左下ノード＝「〈何が正しいか〉の論点」（左マーカー＝相手へ渡す／勲章）
  - 右下ノード＝「〈どう決めるか〉の論点」（右マーカー＝手元に残す／決定権）
- 代替テキスト: 論破型との議論は「何が正しいか」と「どう決めるか」の二つの論点に割れ、前者（正しさの勲章）は相手に丸ごと渡し、後者（決定権）だけを自分の手元に残す——正しさで負けて決定で勝つ、という受け方の骨組み。

### 第4章 マウント型——張り合う人（土俵に上がらず労いで返す）

- ファイル名: `ch04.jpg`
- 挿入位置: ch04.md 見出し「### この型の急所——「価値がない」に触れない」の節内。段落「同じ「俺が徹夜で仕上げた」に、今度は「そのころは……」……その一点にある。この感覚を、次の三本に落とし込んでいく。」の直後、見出し「### 守りの一言、三本」の直前
- 系統: **Before→After（左右対比）**。左3ノード・右3ノード、各列とも下向き矢印2本、中央に細い縦の仕切り線。ループなし
- 図解対象の理由: 「褒めれば穏やかになる」と誤読されやすい章。**「すごいですね」は審判席に座って採点の土俵を開く（火を大きくする）／「大変だったんですね」は労いで土俵の外に立つ（火を絞る）**という、同じ自慢への二通りの火の回り方を対比して固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a before-and-after comparison split into left and right halves
by a thin vertical divider line: on the left, a vertical column of
exactly three rounded rectangular nodes in muted gray tones connected
by exactly two downward arrows, with a small rising flame icon at the
bottom; on the right, a vertical column of exactly three rounded
rectangular nodes in navy and white tones connected by exactly two
downward arrows, with a small shrinking flame icon at the bottom; the
two columns are parallel and not connected, no loop
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F
plus neutral gray for the left half, white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 左列見出し＝「Before: 採点で受ける」
  - 左1＝「自慢が始まる」 / 左2＝「『すごいですね』（審判席に座る）」 / 左3＝「格付け競技が続く（火が大きくなる）」
  - 右列見出し＝「After: 労いで受ける」
  - 右1＝「自慢が始まる」 / 右2＝「『そのころは大変だったんですね』（土俵の外）」 / 右3＝「昔話が閉じる（火が絞られる）」
- 代替テキスト: マウント型の自慢に「すごいですね」で返すと採点の土俵が開いて競技が続き火が大きくなるが、「大変だったんですね」と労いで返すと勝ち負けの軸から外れて話が静かに閉じる、という同じ自慢への二通りの受け方の対比。

### 第5章 被害者型——不機嫌で支配する人（感情の責任者にならない）

- ファイル名: `ch05.jpg`
- 挿入位置: ch05.md 見出し「### 礼儀までは返す、肩代わりからは降りる」の節内。段落「この二つを分けているのは、能力でも根性でもない。……返すのは、礼儀まででいい。」の直後、見出し「### 守りの一言——三つの場面」の直前
- 系統: **構造図（境界線／分離）**。中央に縦の境界線を1本。左＝あなたの領分に上下2ノード、右＝相手の領分に1ノード。左から境界線へ向かう右向き矢印1本は**境界線の手前で止まる**（小さな停止バーで遮る）。ループなし
- 図解対象の理由: 分離応答の「共感は返すが肩代わりはしない」は、文章だと「結局やるのかやらないのか」と混同されやすい。**感情への共感・礼儀は境界線のこちら側で返し、業務の肩代わりは境界線を越えず相手側に残す**という線引きを一枚で固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a single vertical divider line down the middle; on the left
side (your area) exactly two rounded rectangular nodes stacked
vertically; on the right side (the other person's area) exactly one
rounded rectangular node; one arrow starts from the left and points
right toward the divider but is stopped just before it by a small
short perpendicular stop-bar on the line, so it does not cross; no loop,
no other connections
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 境界線＝「感情の責任の境界線」
  - 左上ノード＝「感情への共感『大変そうですね』」
  - 左下ノード＝「礼儀『何かあれば声かけてくださいね』」
  - 右ノード＝「業務の肩代わり『じゃあ私がやります』（相手の領分に残す）」
  - 止まる矢印＝「共感は返すが、肩代わりの手前で止まる（＝分離応答）」
- 代替テキスト: 被害者型には、感情への共感と礼儀は境界線のこちら側で返し、業務の肩代わりは境界線を越えず相手側に残す——共感と肩代わりを切り離す「分離応答」で、相手の感情の責任者にならない、という線引き。

### 第6章 搾取型——押し付ける人（タスクを見える場所に置き、入れ替え交渉に持ち込む）

- ファイル名: `ch06.jpg`
- 挿入位置: ch06.md 見出し「### この型の急所——本当に恐れているもの」の節内。段落「入れ替えの交渉が、その場では持ち込みにくいこともある。……見える場所に引きずり出す。それだけで、押しつけは自動では進めなくなる。」の直後、次段落「もう一段、この受け方の効きめを補っておきたい。」の直前
- 系統: **対処フロー**。直線4ノード、左→右の矢印3本、ループ・分岐なし。最終ノードは境界線が戻る含意で明るめ
- 図解対象の理由: 「断る勇気の話」と誤読されやすい章。**断らずに、抱えているタスクを可視化し、順番の判断を上司に返す（入れ替え交渉）だけで境界線が戻る**という手続きの流れを固定する
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing a straight horizontal flow of exactly four rounded rectangular
nodes connected left to right by exactly three arrows all pointing
right, a straight linear sequence, no loop, no branches; the second
node drawn as a small tray or desk holding two smaller task cards to
suggest visible workload, the last node slightly brighter
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - ノード1＝「追加の押し付けが来る」（補足: 金曜夕方の「ちょっとだけ」）
  - ノード2＝「抱えているA・Bを見せる」（補足: タスクの可視化＝机に並べる）
  - ノード3＝「『どちらを後ろに回しますか』」（補足: 入れ替え交渉／条件付き受諾）
  - ノード4＝「順番の判断を上司に返す」（補足: 断らずに境界線が戻る）
- 代替テキスト: 搾取型には、断らずに、抱えているタスクを見える場所に置き、「どちらを後ろに回しますか」と順番の判断を上司に返す——勇気ではなく事務手続きの反復で境界線を戻す、という受け方の流れ。

### 終章 型は混ざる・切り替わる——見立てと、逃げる判断

- ファイル名: `ch07.jpg`
- 挿入位置: ch07.md 章導入の段落群のうち、段落「切り替わりは、その場の相手で変わるだけではない。……今その一言が、何を運んできたか。そのほうだ。」の直後、見出し「### 型を当てるのが、目的ではない」の直前
- 系統: **構造図（状態遷移サイクル）**。中央に1ノード（同じ一人の上司）。その周囲に5ノードを円環に配置し、**円環の隣どうしを曲がった矢印でつなぐ（サイクル＝切り替わりを示す）**。中央ノードとは線でつながない（第1章の放射マップと差別化：ch01＝中心へ単線・矢印なし／ch07＝外周をめぐる曲線矢印）
- 図解対象の理由: 「上司を一つの型に確定して暗記する本」と誤読されやすい終章に対し、**同じ一人が相手・場面によって五型を切り替える（混ざる）**という結論を一枚で固定する。第1章の静的な地図に対し、こちらは動的な切り替わりを描く
- Gemini プロンプト:

```
A simple flat diagram illustration for a Japanese self-help book,
showing one central rounded node (a single person silhouette) with
exactly five rounded rectangular nodes placed in a ring around it; the
five outer nodes are connected to their neighbors by curved arrows that
form a continuous loop around the ring (a cycle), suggesting switching
between states; the central node is NOT connected to the outer ring by
any line
Style: minimal flat design, 2-3 colors based on deep navy #1F3A5F,
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

- ラベル表:
  - 中央ノード＝「同じ一人の上司」（補足: 誰の前かで切り替わる）
  - 外周ノード（時計回り）＝「高圧型」「論破型」「マウント型」「被害者型」「搾取型」
  - 円環の矢印＝「相手・場面で型が切り替わる（混ざる）」
- 代替テキスト: 現実の上司は五型のどれか一つに固定されず、同じ一人が相手や場面によって高圧・論破・マウント・被害者・搾取のあいだを切り替える——だから確定せず、今この瞬間どの動力源で動いているかだけを見立てる、という終章の要点。

---

## ファイルサイズ試算

表紙1点＋図解7点 × JPEG品質80（図解は白背景フラットで軽い）＝ 合計1.5〜2MB 想定。EPUB 3MB 目安内。点数追加はしない。

---

## 自己チェック（prompts/06_images.md §4）

- [x] 全プロンプト（表紙2本＋図解7本）に `no text, no letters, no numbers` 系のネガティブ指定がある
- [x] 帯色 #1F3A5F はカテゴリ「職場・仕事」のパレット（visual_system.md §2）と一致。アクセントは白。1冊目と同色でシリーズ棚を統一
- [x] 挿入位置はすべて draft の実在の見出し・段落を「見出し名＋段落冒頭／末尾の文言」で特定している（各章で照合済み）
- [x] 代替テキストはすべて「図が伝える内容」（地図・対比・分割・線引き・流れ・切り替わり）で書き、「〜のイラスト」型の画像説明にしていない
- [x] 点数は各章1点×7＋表紙で過剰でない。白背景フラット図解主体で EPUB 3MB 目安内
