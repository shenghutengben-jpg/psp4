"""
クルー（マスタ情報）を表すモデル。

クルーの氏名などの基本情報のみを保持する。
「いつ働くか」という勤務時間は日付によって変わるため、
ここでは持たず Schedule 側で管理する。
"""

from dataclasses import dataclass, asdict


@dataclass
class Crew:
    id: int
    name: str

    def to_dict(self) -> dict:
        """JSON保存用にdict形式へ変換する。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Crew":
        """JSONから読み込んだdictからCrewインスタンスを生成する。"""
        return cls(
            id=data["id"],
            name=data["name"],
        )