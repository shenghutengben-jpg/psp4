from models import Assignment
from repositories._base import load_json_list, save_json_list

FILENAME = "assignments.json"


def load_assignments() -> list[Assignment]:
    raw_list = load_json_list(FILENAME)
    return [Assignment.from_dict(raw) for raw in raw_list]


def save_assignments(assignments: list[Assignment]) -> None:
    raw_list = [assignment.to_dict() for assignment in assignments]
    save_json_list(FILENAME, raw_list)