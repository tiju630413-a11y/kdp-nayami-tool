# Phase 1 自己検証ログ（2026-07-04）

仕様 §10-1 に基づく Phase 1 完了時の自己検証。

## 成果物一覧と検証結果

| 成果物 | 仕様 | 検証 | 結果 |
|---|---|---|---|
| data/genre_map.json | §4.1 300〜500件 | validate_genre_map.py 実行 | **PASS** 330件 / FAIL 0 / WARN 1（判定済み・採用） |
| data/genre_map_parts/*.json | §4.1 | 10カテゴリ全ファイル存在・JSON妥当 | PASS（32〜34件×10、最大最小比1.06） |
| logs/genre_map_validation.md | §4.1 検証ログ | 重複統合・粒度・バランス・再採点の4項目を記録 | PASS |
| data/trends/trend_topics.json | §4.2 | スキーマ定義＋昇格ルール（expires）記載 | PASS（週次観測は運用開始後） |
| templates/book_types/ 型A〜E | §4.3 | 5ファイル。各型に章構成/字数配分/冒頭1000字パターン/締め/NG | PASS |
| templates/kdp_sheet.md | §5-7 | AI申告欄・品質ゲート転記を含む | PASS |
| templates/description.md | §5-8 | 冒頭3行・数字と名前・NGチェック | PASS |
| templates/back_matter.md | §4.3 | 奥付に©・機械学習禁止文・発行日・著者名。レビュー依頼は純粋なお願いのみ | PASS |
| templates/note_article.md / x_posts.md | §5-8 | note2本の型・X5本の役割定義 | PASS |
| style/guide.md | §4.4 | 執筆姿勢＋機械チェック対応の文体規則＋専門家誘導定型文 | PASS |
| style/ng_phrases.txt | §4.4 50〜100語 | 実表現 82 語（コメント行除く） | PASS |
| style/review_checklist.md | §4.4 | 星1理由8系統＋安全規約、全項目に合否基準 | PASS |
| cover/visual_system.md | §4.5 | グリッド/カテゴリ別パレット/文字なしKV/縮小テスト/サイズ管理 | PASS |
| prompts/00_asset_intake.md | §4.6a・§10-5 | 記入例5件つき・1問1答方式・30分20件の設計 | PASS |
| data/author_assets/assets.json | §4.6a | 空配列で初期化（スキーマは intake に定義） | PASS |
| data/competitors/ | §3 | README＋observations.csv（列定義・記入例） | PASS |
| scripts/style_check.py | §4.4 | 下記の単体テスト | **PASS** |
| scripts/validate_genre_map.py | §4.1 | 実行済み・冪等（再実行可能） | PASS |
| config/settings.yaml | §7 | 仕様の全キー＋epub/style_check/kdp 追加 | PASS |

## style_check.py 単体テスト結果

- 正常系原稿（文体ガイド準拠・245字・--min-chars 100）: **PASS / 指摘なし / exit 0**
- 異常系原稿（AI常套句・診断表現・文末3連続・重ね言葉を混入）:
  **FAIL 7件 + WARN 3件 / exit 1** — 文末「です」3連続、NG表現4種、
  診断的表現「あなたは適応障害かも」、断定「必ず治り」、重ね言葉2件を全て検出
- 検出項目8系統（字数/読点密度/文末重複/NG表現/段落長/具体性密度/診断表現/簡易誤字）実装済み

## genre_map 検証の要点（logs/genre_map_validation.md より）

- 総数330・ID重複0・pain完全重複0・adjacent_ids参照切れ0・スキーマ欠落0
- 大分類バランス: 32〜34件/カテゴリ（最大最小比 1.06 ≤ 1.5）
- evergreen 分布は4-5が大半、時事依存エントリは notes に二層構造の扱いを明記
- 医療・法律・金銭に接するエントリは notes に「断定回避・専門家誘導必須」を記録

## 残課題（Phase 1 時点）

- 著者資産が0件（運用初日に prompts/00_asset_intake.md で20件投入が必要。
  これが無いと plan 工程の資産割当が動かない）
- adjacent_ids のカテゴリ横断リンクは未整備（D-02、運用中に追記）
- trend_topics.json の第1回観測は運用開始週に実施
