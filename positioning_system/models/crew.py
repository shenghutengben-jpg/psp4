# models/crew.py
from dataclasses import dataclass

@dataclass
class Crew:
    id: int
    name: str
    start_time: str
    end_time: str