from dataclasses import dataclass


@dataclass
class Assignment:
    id: int
    date: str
    time_slot_id: int
    position_id: int
    crew_id: int