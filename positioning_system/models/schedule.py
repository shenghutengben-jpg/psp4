"""
特定の日付における、特定クルーの勤務予定を表すモデル。

Crew自体は氏名などのマスタ情報のみを持ち、
「その日、何時から何時まで働くか」はこのSchedule側で管理する。
同じクルーでも日によって勤務時間が変わるため、
CrewとScheduleをあえて分けて設計している。
"""

from dataclasses import dataclass, asdict


@dataclass
class Schedule:
    id: int
    date: str        # "YYYY-MM-DD" 形式
    crew_id: int
    start_time: str  # "HH:MM" 形式
    end_time: str     # "HH:MM" 形式

    def to_dict(self) -> dict:
        """JSON保存用にdict形式へ変換する。"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Schedule":
        """JSONから読み込んだdictからScheduleインスタンスを生成する。"""
        return cls(
            id=data["id"],
            date=data["date"],
            crew_id=data["crew_id"],
            start_time=data["start_time"],
            end_time=data["end_time"],
        )