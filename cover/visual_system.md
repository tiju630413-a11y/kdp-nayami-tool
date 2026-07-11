# シリーズ視覚言語（cover/visual_system.md）

画像生成はユーザーが Gemini で実行する。ツール側は
「Geminiプロンプト＋配置指定＋チェックリスト」を出す（prompts/06_images.md が使用）。
目的は棚での統一感＝著者ブランド認知。1冊ごとにデザインを発明しない。

---

## 1. 共通レイアウトグリッド（全シリーズ固定）

KDP表紙推奨サイズ: 1600 x 2560 px（縦横比 1:1.6）。

```
+--------------------------------+
| 上部 12%: シリーズ帯            |  ← シリーズ名＋番号（例: 智珠の処方箋 03）
+--------------------------------+
|                                |
| 中央 55%: キービジュアル領域    |  ← Gemini生成（文字なし）
|                                |
+--------------------------------+
| タイトル帯 25%:                 |  ← 単色ベタ帯＋タイトル文字
|   メインタイトル（最大13字/行） |
|   サブタイトル（1行）           |
+--------------------------------+
| 下部 8%: 著者名「智珠」         |  ← 右寄せ、白 or 帯色の濃色
+--------------------------------+
```

- タイトル帯は**単色ベタ**（カテゴリ色）。ビジュアルに文字を重ねない。
  帯の上に白文字（または濃色文字）で最大コントラストを取る。
- メインタイトルは 1〜2 行、1行 13 字以内。3行になるタイトルは title 工程に差し戻す。
- シリーズ番号は 2 桁ゼロ埋め（01, 02…）。

## 2. カテゴリ別カラーパレット（帯色・アクセント色）

| カテゴリ | 帯色 | HEX | アクセント |
|---|---|---|---|
| 職場・仕事 | ネイビー | #1F3A5F | 白 |
| 人間関係全般 | ティール | #2A6E6A | 白 |
| 恋愛 | ローズ | #B5495B | 白 |
| 夫婦・家族 | テラコッタ | #B0603D | 白 |
| 子育て | アンバー | #C98A2D | 濃茶 #3B2A1A |
| お金・生活防衛 | ディープグリーン | #2E5D3A | 白 |
| メンタル・自己肯定感 | ラベンダー | #6B5B95 | 白 |
| コミュニケーション・話し方 | コーラルオレンジ | #D2603A | 白 |
| 習慣・私生活 | スレートブルー | #4A6FA5 | 白 |
| ライフイベント | ボルドー | #6E2B3A | 白 |

同カテゴリ内の続刊は帯色固定・キービジュアルだけ変える（棚で「同じ著者の別の1冊」と分かる）。

## 3. 文字なしキービジュアル方式

- Gemini には**文字を含まない**背景・メインビジュアルのみ生成させる。
  タイトル文字はユーザーが後から重ねる（Canva等。AI画像の文字崩れ回避の定石）。
- ビジュアルの方向性: フラットイラスト調で統一（写真調は使わない。
  シリーズ間の質感ブレが出やすく、人物写真は「誰?」問題を生む）。
  夜・室内・後ろ姿・手元など「読者の孤独な場面」をモチーフにする。

### Geminiプロンプト雛形（表紙キービジュアル）

```
A flat vector illustration for a Japanese self-help book cover.
Scene: {場面の指定。例: a person sitting alone on a bed at night,
looking at a smartphone, room lit only by the screen}
Mood: quiet, empathetic, slightly hopeful
Color scheme: muted tones harmonizing with {カテゴリ帯色 HEX},
plenty of negative space in the upper and lower thirds
Composition: main subject in the center, simple background
Style: modern flat illustration, soft edges, no gradients overload
IMPORTANT: no text, no letters, no numbers, no typography,
no watermark, no signature, no logo
Aspect ratio: 5:8 (vertical)
```

### 本文挿絵・図解の雛形（各章1点目安）

種類は3系統。images 工程は各章にどれを使うか指定して出力する。
1. **悩みの構造図**: 悪循環ループ・要因の分解（フラットなダイアグラム風）
2. **対処フロー**: ステップ図（1→2→3）
3. **Before→After 場面イラスト**: 左右対比 or 上下対比

```
A simple flat diagram illustration for a Japanese self-help book,
showing {構造の指定。例: a cycle of overthinking: trigger → rumination
→ self-blame → insomnia, drawn as a circular loop with 4 nodes}
Style: minimal flat design, 2-3 colors based on {帯色HEX},
white background, clean lines
IMPORTANT: no text, no letters, no numbers (labels will be added later)
Aspect ratio: 4:3 (horizontal)
```

※図解のラベル文字も後から重ねる。ノード数・矢印の向きをプロンプトで固定する。

## 4. スマホ縮小視認テスト（表紙の合格条件）

表紙画像を **幅 90px** に縮小して確認する（Amazonの検索結果サムネ相当）:

- [ ] メインタイトルが読める（読めない→帯を太く・文字を大きく・字数を削る）
- [ ] 何の悩みの本か、ビジュアルだけで1秒で分かる
- [ ] 帯色がカテゴリパレットと一致している
- [ ] 隣に他社の本が並んだ想定で、埋没しない（コントラスト確認）
- [ ] シリーズ既刊と並べたとき「同じシリーズ」と分かる

縮小コマンド例: `python3 -c "from PIL import Image; Image.open('cover.jpg').resize((90,144)).save('thumb_test.png')"`

## 5. ファイルサイズ管理

- 表紙: JPEG品質80・幅1600px以下（build_epub.py が自動圧縮）
- 本文挿絵: 幅1200px以下・JPEG品質80（同上）
- EPUB合計 2〜3MB 以下目安（KDPの配信コストはロイヤリティから差し引かれる）。
  3MB超過で build_epub.py が WARN、3.5MB超で FAIL。
