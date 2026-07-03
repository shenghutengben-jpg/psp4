import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "positions.json"
    
def load_positions():
    if not DATA_PATH.exists():
        return []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_positions(positions):
    DATA_PATH.parent.mkdir(exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(positions, f, ensure_ascii=False, indent=2)