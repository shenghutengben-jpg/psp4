"""
Repository層の共通処理。

各Repositoryファイルからは、
「どのJSONファイルを」「どのモデルクラスとして」扱うかだけを
指定すればよいようにするための土台。
"""

import json
from pathlib import Path

# このファイル（repositories/_base.py）から見て
# 一つ上の階層をプロジェクトルートとみなす
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json_list(filename: str) -> list[dict]:
    """
    data/<filename> を読み込み、dictのリストとして返す。
    ファイルが存在しない場合は空リストを返す（初回起動時など）。
    """
    path = DATA_DIR / filename

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_list(filename: str, items: list[dict]) -> None:
    """
    dictのリストを data/<filename> へ保存する。
    dataフォルダ自体が存在しない場合も、親フォルダごと作成する
    （parents=Trueにより、data の親フォルダが無くてもエラーにならない）。
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    path = DATA_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)