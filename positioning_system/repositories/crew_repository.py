from models import Crew
from repositories._base import load_json_list, save_json_list

FILENAME = "crews.json"


def load_crews() -> list[Crew]:
    raw_list = load_json_list(FILENAME)
    return [Crew.from_dict(raw) for raw in raw_list]


def save_crews(crews: list[Crew]) -> None:
    raw_list = [crew.to_dict() for crew in crews]
    save_json_list(FILENAME, raw_list)