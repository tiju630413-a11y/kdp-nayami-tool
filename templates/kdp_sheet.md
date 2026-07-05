# KDP 登録シート ── 必要フィールド定義（templates/kdp_sheet.md）

scripts/kdp_sheet.py が book.json / kdp_meta.json / promo/description.md / 実測値から
`output/NNN_kdp_sheet.md`（全項目版）を生成する。生成物はKDPの各入力欄に転記できる。
このファイルは「各データファイルに何を用意すべきか」の定義。

## books/NNN/book.json に必要なフィールド

| キー | 例 | 用途 |
|---|---|---|
| title / subtitle | 職場の理不尽から自分を守る台本36 / 言い返せなくていい… | ②③ |
| title_kana / subtitle_kana | ショクバノリフジン… | KDPフリガナ欄（必須） |
| title_romaji / subtitle_romaji | Shokuba no rifujin… | Author Central 参考 |
| title_en | 36 Scripts to… | 英題（任意） |
| series_name / series_number | 今夜の処方箋 / 1 | ④（空なら単独タイトル扱い） |
| edition | 1 | ⑤版数 |
| author | 智珠 | ⑥（姓欄に入れ名欄は空） |
| author_kana / author_romaji | チジュ / Tiju | ⑥フリガナ・ローマ字（著者ブランドと統一） |
| copyright_romaji | Tiju | 奥付©（build_epub が使用） |
| note_url / x_url | https://note.com/tiju630413 / https://x.com/Tiju003 | 巻末SNS導線・シート |
| adult_content / age_rating / drm | いいえ / 一般 / なし | ⑪⑫ |
| publish_date | 空可（出版日にKDP付与） | 奥付・日付 |

## books/NNN/kdp_meta.json に必要なフィールド

- `keywords`: 7個（タイトル・サブ語と重複させない）
- `keywords_rationale`: 選定根拠（1文）
- `categories`: 最大3個。各 `{"jp": "...", "en": "..."}`
- `categories_note`: 申請制注意など

## promo/description.md

KDPの内容紹介そのもの（最大約4,000字・`<br><b><i>` 可）。
templates/description.md の型に従い、冒頭フック→痛み→反転→◆ベネフィット5〜6→
【こんな方へ】→【本書について】。固有の武器（台本数・命名FW・二の手）を数字と名前で。

## 生成と再生成

```
python3 scripts/kdp_sheet.py NNN
```
不足フィールドは上記2ファイルに追記して再実行。AI開示・価格帯・カテゴリはKDP仕様変更が
あるため、生成物冒頭の注意書きどおり登録時に最新の公式ガイドを確認する。
