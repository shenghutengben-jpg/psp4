# models/time_slot.py
from dataclasses import dataclass

@dataclass
class TimeSlot:
    id: int
    start_time: str
    end_time: str