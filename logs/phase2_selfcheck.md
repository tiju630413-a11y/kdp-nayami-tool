# Phase 2 自己検証ログ（2026-07-05）

仕様 §10-1 に基づく Phase 2（パイプライン9工程）完了時の自己検証。
検証方法: ダミー書籍 `001_test_smoke` で plan→promo→retro を実走し、
全スクリプト・全分岐を通した（検証後にテストデータは削除、コードのみ残置）。

## 成果物一覧と検証結果

| 成果物 | 仕様 | 検証内容 | 結果 |
|---|---|---|---|
| prompts/01_plan.md | §5-1 | 多軸スコア5軸＋時事ボーナス・断言欄必須・資産フィルタ（max_asset_reuse除外）・リジェクト条件 | PASS（記載確認） |
| prompts/01b_title.md | §5-1b | 10案生成の方向性配分・採点5軸・上位2案＋サブタイトル | PASS |
| prompts/02_outline.md | §5-2 | 型選択・章別字数配分（4万字下限）・資産割当・タイトル回収対応表 | PASS |
| prompts/03_draft.md | §5-3 | 文体ガイド・資産注入・章単位執筆・assets_used 記録 | PASS |
| prompts/04_review_loop.md | §5-4, §10-3 | 6観点の観点表＋重大指摘基準・収束条件（重大ゼロ/最大3周/エスカレーション）・baseline実生成手順・観点別コンテキスト分離 | PASS |
| prompts/05_style.md | §5-5 | style_check 全PASS まで・内容不改変の原則・音読パス | PASS |
| prompts/06_images.md | §5-6 | Geminiプロンプト＋挿入位置＋代替テキストのセット出力 | PASS |
| prompts/08_promo.md | §5-8 | 紹介文（数字と名前）・note2本・X5本の役割固定 | PASS |
| prompts/09_retro.md | §5-9 | 倍賭け/撤退・推奨ペース（律速3指標＋資産残量）・一発OK還流ブロック | PASS |
| scripts/pipeline.py | §5 | 下記の実走テスト | **PASS** |
| scripts/build_epub.py | §5-7, §4.5 | 下記の実走テスト | **PASS** |
| scripts/kdp_sheet.py | §5-7 | 実走・AI申告「あり」含む・未充填検出 | PASS |
| scripts/import_kdp.py | §5-9 | sales/kenp CSV・register・review・冪等取込 | PASS |
| scripts/retro.py | §5-9 | KPI集計・スループット記録・資産プール残量・--summary | PASS |
| scripts/_common.py | - | 設定読み（PyYAML有無両対応）・書籍探索・字数計測 | PASS |
| README.md | §10-7・依頼7 | スマホ定型指示集 / Opus引き継ぎ手順 / 一発OK還流ルール | PASS |

## 実走テストの記録（001_test_smoke）

1. `pipeline new` → ワークスペース生成（draft/reviews/images/promo/_work）OK
2. `pipeline status/next` → 工程判定と実行指示書の生成 OK
3. `pipeline review --round 1` → 観点別指示書6枚生成（baseline 必須チェック動作）
4. `--collect`: 重大1件 → 未収束・round2 案内 / 重大0 → converged.md 生成・
   logs/reviews_NNN.md へ周回記録。max_review_loops 到達時の escalation 分岐はコードレビューで確認
5. `build_epub` → book.json 雛形出力 → 記入後ビルド成功。
   EPUB構造検証: mimetype無圧縮先頭・container/opf/nav/全xhtmlのXML妥当性・
   表紙/挿絵の格納を機械検証 OK。画像圧縮動作（cover 98KB→23KB, 挿絵 29KB→6KB）
6. `kdp_sheet` → kdp_meta 雛形→7キーワード検証→シート生成（AI申告「あり」含む）
7. `pipeline gate` → 10項目判定。ダミー原稿で FAIL 2件（字数不足・style_check）
   ＝**不合格品を正しくブロック**。PASS項目8件は実データで成立
8. `import_kdp` → sales 2行・kenp 1行取込（UNIQUE制約で再取込冪等）・
   register・review 記録 → `show` で集計一致
9. `retro log` ＋ `retro` → 週次レトロ生成（売上/KENP/レビュー/スループット/
   資産プール残量「あと約N冊分」）。`--summary` OK
10. `assets-sync` → used_in 反映 10件 OK

## 実走で見つけて直した問題（還流）

- **gate 項目8（奥付）**: 草稿を検査していたが奥付は build が EPUB 巻末に
  生成するため常に FAIL になる欠陥 → EPUB 内 back.xhtml を検査するよう修正
- **retro の「今月」計算**: 月またぎ週で前月扱いになる → 週の終了日
  （日曜レトロ実行日側）の月を採用するよう修正

## 残課題（Phase 2 時点）

- pipeline の review 指示書は生成するが、サブエージェント起動自体は
  運用側（Claude Code）の操作。README の定型指示でカバー
- import_kdp の列名自動推定は実際の KDP レポートで初回に要確認
  （ズレたら --col-* で明示指定できる）
