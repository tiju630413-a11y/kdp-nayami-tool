# 実行指示書: 001_iikaesenai / 工程 review_loop round1（枠切れ引き継ぎ）

状態（2026-07-05 時点・すべてコミット済み）:
- draft 全9章完了（41,647字・台本36本・結合style_check PASS・資産24件使用）
- baseline.md 生成済み / reviews/round1/*_task.md 6枚生成済み
- モデル枠切れにより6観点レビューが未実行で停止

## 再開手順（どのモデルでも可・README「Opus 4.8への引き継ぎ手順」参照）

1. reviews/round1/ の6枚の *_task.md を、**それぞれ独立したコンテキスト
   （別セッション or サブエージェント）**で実行し、*_findings.md を保存させる
   （同一会話で6観点を連続実行しない。ai_substitute には baseline との
   章別○△×比較表を必ず作らせる）
2. `python3 scripts/pipeline.py review 001 --round 1 --collect` で集計
3. 重大指摘あり → 改稿（別コンテキスト推奨）→ revision_notes.md →
   `pipeline.py review 001 --round 2` で再走（最大3周）
4. 収束後: prompts/05_style.md（style_pass）→ prompts/06_images.md →
   build（book.json: title=職場の理不尽から自分を守る台本36 /
   subtitle=言い返せなくていい。「守りの一言」だけ持っていく /
   series=今夜の処方箋 01）→ kdp_sheet → promo
