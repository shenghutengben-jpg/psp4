"""
ポジション（マスタ情報）を表すモデル。

例: レジ、ドライブスルー、ポテト、ハンバーガー作成 など。
ポジション名は自由に設定できる。
"""

from dataclasses import dataclass, asdict


@dataclass
class Position:
    id: int
    name: str

    def to_dict(self) -> dict:
        """JSON保存用にdict形式へ変換する。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Position":
        """JSONから読み込んだdictからPositionインスタンスを生成する。"""
        return cls(
            id=data["id"],
            name=data["name"],
        )