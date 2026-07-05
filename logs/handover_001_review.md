# 引き継ぎ: 001 review round3（枠切れ・2回目）

状態（コミット済み）:
- round1: 重大18 → 改稿で全対応 / round2: 重大5 → 改稿で全対応（47,546字・PASS）
- round3: reviews/round3/*_task.md 6枚生成済み・findings 未実行（枠切れ、10:00 UTC リセット）

再開手順:
1. round3 の6枚の task を独立コンテキストで実行（ai_substitute は baseline との章別○△×表を必須）
2. python3 scripts/pipeline.py review 001 --round 3 --collect
   → 重大0なら収束（converged.md 自動生成）/ 残れば escalation.md（人間判断へ）
3. 収束後: prompts/05_style.md → 06_images → build（book.json: title=職場の理不尽から自分を守る台本36 / subtitle=言い返せなくていい。「守りの一言」だけ持っていく / series=今夜の処方箋 / series_number=1）→ kdp_sheet → promo
