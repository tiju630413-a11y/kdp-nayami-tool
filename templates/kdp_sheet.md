# KDP 登録シート（templates/kdp_sheet.md）

scripts/kdp_sheet.py が books/NNN/plan.md・promo/ から値を差し込んで
output/NNN_kdp_sheet.md を生成する。KDP管理画面にこの順で転記すれば登録が終わる。

---

## 基本情報

| 項目 | 値 |
|---|---|
| タイトル | {{title}} |
| サブタイトル | {{subtitle}} |
| シリーズ名（KDPシリーズ登録） | {{series_name}} |
| シリーズ番号 | {{series_number}} |
| 著者名 | 智珠 |
| 言語 | 日本語 |

## 紹介文（そのまま貼り付け）

{{description}}

## キーワード（7個）

| # | キーワード |
|---|---|
| 1 | {{keyword_1}} |
| 2 | {{keyword_2}} |
| 3 | {{keyword_3}} |
| 4 | {{keyword_4}} |
| 5 | {{keyword_5}} |
| 6 | {{keyword_6}} |
| 7 | {{keyword_7}} |

## カテゴリ（2個）

| # | カテゴリ |
|---|---|
| 1 | {{category_1}} |
| 2 | {{category_2}} |

## 価格・配信

| 項目 | 値 |
|---|---|
| 価格 | {{price_yen}}円 |
| KDPセレクト | 加入する |
| DRM | なし |
| 原稿ファイル | {{epub_file}} |
| 表紙ファイル | {{cover_file}} |

## AI生成コンテンツ申告（必須・「あり」以外で登録しない）

| 項目 | 申告 |
|---|---|
| テキスト: AIツールで生成しましたか | **あり**（AIツールで生成し、大幅な編集を加えた） |
| 画像: AIツールで生成しましたか | **あり**（AIツールで生成し、大幅な編集を加えた） |

## 出版前 最終チェック（品質ゲート §8 の転記。全て YES になるまで登録しない）

- [ ] 総字数 40,000 字以上（style_check PASS）
- [ ] review_loop 収束（重大指摘ゼロ・{{review_loops}}周で収束）
- [ ] AI代替判定 合格（baseline.md 比較済み）
- [ ] 著者資産 {{assets_used}} 件採用（最低 {{min_author_assets}} 件）
- [ ] style_check 全項目 PASS
- [ ] 医療・法律・金銭の断定なし＋専門家誘導定型 挿入済み
- [ ] AI生成申告 = テキスト/画像とも「あり」
- [ ] 巻末に奥付・著作権表記あり
- [ ] 表紙: シリーズ視覚言語準拠＋スマホ縮小視認テスト OK
- [ ] EPUBサイズ {{epub_size_mb}} MB（3MB以下目安）
- [ ] 今週の出版数が pace_per_week（{{pace_per_week}}冊）以内・KDP週10上限以内
- [ ] 人間の通読 1回 完了（修正が出た場合: 資産側への還流 済 / 内容: {{feedback_note}}）
