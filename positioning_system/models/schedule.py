from dataclasses import dataclass


@dataclass
class Schedule:
    id: int
    date: str
    crew_id: int
    start_time: str
    end_time: str