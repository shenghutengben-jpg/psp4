from models import Schedule
from repositories._base import load_json_list, save_json_list

FILENAME = "schedules.json"


def load_schedules() -> list[Schedule]:
    raw_list = load_json_list(FILENAME)
    return [Schedule.from_dict(raw) for raw in raw_list]


def save_schedules(schedules: list[Schedule]) -> None:
    raw_list = [schedule.to_dict() for schedule in schedules]
    save_json_list(FILENAME, raw_list)