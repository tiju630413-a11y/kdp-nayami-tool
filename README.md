# KDP悩み系出版支援ツール

悩み系（人間関係・職場・恋愛・夫婦家族・お金・メンタル等）のKindle出版を、
企画→執筆→出版→販促→改善まで一気通貫で支援するツール。
仕様書: `fable5_build_spec_kdp_nayami.md`（v3.2）/ 構築時の判断: `logs/decisions.md`

- 運用者1人・ペンネーム「智珠」・note (marvelous1101) / X 連携
- 知識はデータに（data/・style/・templates/）、手順はプロンプトに（prompts/）、
  検査はスクリプトに（scripts/）。**モデルを差し替えても資産は残る**
- 品質ゲート（下記10項目）を通らない原稿は出版しない。ペースは変えても
  ゲートは変えない

## 初日にやること（30分）

1. **著者資産の投入（最優先）**: Claude に
   「prompts/00_asset_intake.md を読んで資産聞き取りをして」と言う。
   目標20件。**資産ゼロでは企画工程が動かない**
2. 1冊目を開始: 「企画会議をして」（下の定型指示集を参照）

## 📱 スマホからの定型指示集

日常操作はこの一言をコピペ（または言い換え）するだけで回る。
Claude が対応するプロンプト・スクリプトを読んで実行する。

### 毎日〜随時

| やること | スマホから送る一言 |
|---|---|
| 資産の補充（すきま時間） | 「資産聞き取り。1問ずつ、10分だけ」 |
| 進捗確認 | 「003の進捗は?」（→ pipeline status） |
| 次の作業を進める | 「003の次の工程を進めて」（→ pipeline next → 該当プロンプト実行） |
| 草稿の続き | 「003の続きの章を書いて」 |
| レビューを回す | 「003のレビューを回して。観点は別々のコンテキストで」 |
| 文体仕上げ | 「003の style_pass をして」 |
| 画像プロンプト | 「003の画像プロンプト一式を出して」（→ 出力を Gemini に貼る） |
| ビルド〜登録シート | 「003をビルドして登録シートまで出して」 |
| 販促パック | 「003の販促パックを作って」 |
| ゲート確認 | 「003は出版していい状態? ゲートを見せて」 |

### 週次（日曜・KDP枠リセット後）

| やること | スマホから送る一言 |
|---|---|
| 週次レトロ | 「KDPレポートを取り込んだ。週次レトロして」（CSVを渡す） |
| 企画選定 | 「企画会議をして。今週の◯冊を選んで」 |
| トレンド観測 | 「今週のトレンド観測をして trend_topics に追記して」 |
| 競合観測 | 「このキーワードの競合を観測したい: ◯◯」（結果をCSVに追記させる） |

### 通読後（品質ゲート10・一発OK還流）

| 状況 | スマホから送る一言 |
|---|---|
| 修正ゼロ | 「003通読した。修正ゼロ。一発OKで記録して」 |
| 修正あり | 「003通読した。修正2件: ①第3章の◯◯が説明くさい ②△△が重複。直して、原因を資産側に還流して」 |

### レビュー・売上が動いたとき

| 状況 | 一言 |
|---|---|
| レビューが付いた | 「003に★2レビュー。本文: 『…』。記録して、チェックリストに還流すべきか判断して」 |
| 出版した | 「003を出版した。DBに登録して」 |

## 週次運用サイクル

- **通常モード（週1〜2冊・現設定）**: 日=レトロ＋企画 / 月〜水=執筆・レビュー /
  木=画像・ビルド / 金=出版・販促 / 土=媒体運用・資産補充
- **バッチモード（週10冊）**: 仕様書 §9 参照。増速は retro の推奨に従い
  +1〜2冊/週ずつ（settings.yaml の pace_per_week を人間が変更する）

## パイプライン（9工程）

```
plan → title → outline → (baseline) → draft → review_loop → style_pass
  → images → build → promo → [出版] → retro
```

各工程の詳細は `prompts/`（01〜09）。工程の状態管理・レビューの観点分離・
品質ゲートは `scripts/pipeline.py`:

```bash
python3 scripts/pipeline.py new <slug>       # 新規企画ワークスペース
python3 scripts/pipeline.py status <NNN>     # 進捗と次工程
python3 scripts/pipeline.py next <NNN>       # 次工程の実行指示書を生成
python3 scripts/pipeline.py review <NNN> --round R [--collect]  # レビュー指示書/収束判定
python3 scripts/pipeline.py gate <NNN>       # 品質ゲート（§8）機械検査
python3 scripts/pipeline.py assets-sync <NNN># 資産の used_in 反映
python3 scripts/style_check.py <原稿.md>     # 文体チェック単体
python3 scripts/build_epub.py <NNN>          # EPUB（画像圧縮込み）
python3 scripts/kdp_sheet.py <NNN>           # KDP登録シート
python3 scripts/import_kdp.py sales|kenp <csv> / register <NNN> / review <NNN> --stars N
python3 scripts/retro.py [--summary] / log --readthrough-min N ...
python3 scripts/validate_genre_map.py        # genre_map 追記後の再検証
```

依存: Python 3.9+（標準ライブラリのみで動作）。`pip install pillow` で
EPUB画像圧縮が有効化（無くても動くが圧縮スキップ・WARN表示）。

## 品質ゲート（出版条件・全て必須）

1. 総字数4万字以上（水増し禁止） 2. review_loop 収束＋星1逆算全項目
3. AI代替判定合格（baseline実生成比較） 4. 著者資産10件以上
5. style_check 全PASS 6. 医療・法律・金銭の断定回避＋専門家誘導
7. AI生成申告「あり」 8. 奥付・著作権表記 9. 表紙視認テスト＋EPUB 3MB以下
10. 人間の通読1回（修正ゼロ=一発OK。修正が出たら還流してから次へ）

## 一発OK還流ルール（人間の指摘 → 資産更新）

**目的: 同種の指摘が二度と人間に到達しないこと。** 通読・レビュー・
低評価で人間が見つけた問題は、直すだけで終わらせない。必ず次のどれかを更新する:

| 指摘の種類 | 還流先 |
|---|---|
| AIっぽい言い回し・常套句 | `style/ng_phrases.txt` に追記（次から機械検出） |
| 文体・トーン・構成の癖 | `style/guide.md` に規則として明文化 |
| 読者体験の欠陥（薄い・説教・実践不能 等） | `style/review_checklist.md` に判定基準を追加 |
| 工程の抜け・指示の曖昧さ | 該当する `prompts/*.md` を修正 |
| 機械で検出できるもの | `scripts/style_check.py` にパターン追加 |

手順: ①指摘を直す → ②還流先を決めて更新 → ③`books/NNN/human_readthrough.md`
に「修正N件・還流先」を記録 → ④次の企画へ。
**未還流の修正が残っている間は、次の企画に着手しない**（retro がブロックを宣言する）。

## Opus 4.8 への引き継ぎ手順（Fable 枠切れ時 / 2026-07-08以降）

このツールはモデル非依存で設計されている（プロンプト外部化・状態はファイル）。
引き継ぎに必要なのは以下だけ:

1. **モデルを切り替えるだけで、コマンドとプロンプトはそのまま使える**。
   プロンプト内にモデル名は書かれていない。工程別の推奨モデルは
   `config/settings.yaml` の models（plan/promo=Sonnet 5, draft/review=Opus 4.8,
   routine=Haiku 4.5）
2. 作業中の書籍があれば `python3 scripts/pipeline.py status <NNN>` で
   現在地を確認し、`next` の指示書どおりに続きから実行する
   （工程の状態は全て books/NNN_*/ 内のファイルで判定される。
   会話履歴に依存する状態は存在しない）
3. 新しいセッションの最初に読ませるもの:
   `README.md`（このファイル）→ `logs/decisions.md` → 作業対象の
   `books/NNN_*/plan.md`。全部で5分
4. review_loop の観点分離は引き継ぎ後も厳守（6観点を同一会話でやらない）
5. baseline 生成は「素の別コンテキスト」で（プロジェクトを読ませない）
6. 通読で修正が出たら、上の還流ルールを回してから次へ

## ディレクトリ

```
config/     設定（ペース・価格・字数下限・モデル割当）
data/       genre_map（悩みマップ330件）/ trends / author_assets / competitors / performance.db
prompts/    工程別プロンプト 00〜09（モデル非依存）
templates/  本の型A〜E / KDP登録シート / 紹介文 / 巻末 / note / X
style/      文体ガイド / NG常套句 / 星1逆算チェックリスト
cover/      シリーズ視覚言語（表紙の共通設計）
scripts/    pipeline / style_check / build_epub / kdp_sheet / import_kdp / retro
books/      作品ワークスペース（NNN_slug/）
logs/       検証ログ・レビューログ・レトロ・判断記録
output/     完成EPUB・登録シート
```

## 運用上の注意（規約）

- 出版ペースは KDP 上限（週10タイトル・日曜9:00リセット）内で
  `pace_per_week` 管理。上限張り付き運用は増速データが揃うまでしない
- AI生成申告（テキスト・画像とも「あり」）は登録シートの必須項目
- レビュー依頼は巻末の純粋なお願いのみ（特典交換は規約違反）
- 医療・法律・金銭は断定回避＋専門家誘導（style_check が検出）
