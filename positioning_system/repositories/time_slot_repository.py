from models import TimeSlot
from repositories._base import load_json_list, save_json_list

FILENAME = "time_slots.json"


def load_time_slots() -> list[TimeSlot]:
    raw_list = load_json_list(FILENAME)
    return [TimeSlot.from_dict(raw) for raw in raw_list]


def save_time_slots(time_slots: list[TimeSlot]) -> None:
    raw_list = [time_slot.to_dict() for time_slot in time_slots]
    save_json_list(FILENAME, raw_list)