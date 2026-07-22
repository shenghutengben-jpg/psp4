"""
時間帯（マスタ情報）を表すモデル。

例: "09:00"〜"10:00" のような1時間単位の枠。
特定の日付に紐づくものではなく、共通のマスタとして扱う。
"""

from dataclasses import dataclass, asdict


@dataclass
class TimeSlot:
    id: int
    start_time: str  # "HH:MM" 形式
    end_time: str     # "HH:MM" 形式

    def to_dict(self) -> dict:
        """JSON保存用にdict形式へ変換する。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TimeSlot":
        """JSONから読み込んだdictからTimeSlotインスタンスを生成する。"""
        return cls(
            id=data["id"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )