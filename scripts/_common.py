"""スクリプト共通ヘルパ（標準ライブラリのみ）。

settings.yaml の読み込みは PyYAML があれば使い、なければ
「キー: 値」1段＋2段ネストだけを読む簡易パーサで代替する
（本ツールの settings.yaml はその範囲しか使わない）。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_settings():
    path = ROOT / "config" / "settings.yaml"
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        pass
    cfg, section = {}, None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                section = key
                cfg[key] = {}
            else:
                section = None
                cfg[key] = _coerce(val)
            continue
        m = re.match(r"^\s{2}(\w+):\s*(.*)$", line)
        if m and section:
            cfg[section][m.group(1)] = _coerce(m.group(2).strip())
    return cfg


def _coerce(v):
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def find_book(nnn):
    """'003' や 3 から books/003_* ディレクトリを返す。"""
    nnn = f"{int(nnn):03d}"
    hits = sorted((ROOT / "books").glob(f"{nnn}_*"))
    if not hits:
        raise SystemExit(f"books/{nnn}_* が見つからない")
    if len(hits) > 1:
        raise SystemExit(f"books/{nnn}_* が複数ある: {[h.name for h in hits]}")
    return hits[0]


def combined_manuscript(book_dir, include_front_back=True):
    """draft/ch*.md を番号順に結合したテキストを返す。"""
    drafts = sorted((book_dir / "draft").glob("ch*.md"))
    if not include_front_back:
        drafts = [d for d in drafts if not d.name.startswith(("ch00", "ch99"))]
    return "\n\n".join(d.read_text(encoding="utf-8") for d in drafts), drafts


def char_count(text):
    """空白・見出し記号・コードブロックを除いた本文字数。"""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = "\n".join(l for l in text.splitlines() if not l.startswith("#"))
    return len(re.sub(r"\s", "", text))


def load_assets():
    path = ROOT / "data" / "author_assets" / "assets.json"
    return json.loads(path.read_text(encoding="utf-8"))


def save_assets(assets):
    path = ROOT / "data" / "author_assets" / "assets.json"
    path.write_text(json.dumps(assets, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
