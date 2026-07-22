"""
特定の日付・時間帯・ポジションへの、クルーの配置を表すモデル。

Crew・TimeSlot・Position の3者を結びつける中間的なエンティティ。
「同じ日付・時間帯・ポジションには1人しか配置できない」という
制約は、Assignment自体ではなく assignment_controller 側で担保する
（モデルはあくまでデータの入れ物であり、業務ルールは持たせない）。
"""

from dataclasses import dataclass, asdict


@dataclass
class Assignment:
    id: int
    date: str          # "YYYY-MM-DD" 形式
    time_slot_id: int
    position_id: int
    crew_id: int

    def to_dict(self) -> dict:
        """JSON保存用にdict形式へ変換する。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Assignment":
        """JSONから読み込んだdictからAssignmentインスタンスを生成する。"""
        return cls(
            id=data["id"],
            date=data["date"],
            time_slot_id=data["time_slot_id"],
            position_id=data["position_id"],
            crew_id=data["crew_id"],
        )