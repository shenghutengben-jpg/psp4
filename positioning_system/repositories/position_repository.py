from models import Position
from repositories._base import load_json_list, save_json_list

FILENAME = "positions.json"


def load_positions() -> list[Position]:
    raw_list = load_json_list(FILENAME)
    return [Position.from_dict(raw) for raw in raw_list]


def save_positions(positions: list[Position]) -> None:
    raw_list = [position.to_dict() for position in positions]
    save_json_list(FILENAME, raw_list)