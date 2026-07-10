from repositories.assignment_repository import load_assignments
from repositories.crew_repository import load_crews
from repositories.time_slot_repository import load_time_slots
from repositories.position_repository import load_positions


def find_by_id(items, item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def print_assignments_readable():
    assignments = load_assignments()
    crews = load_crews()
    time_slots = load_time_slots()
    positions = load_positions()

    print("=== 配置情報（見やすい表示） ===")

    for assignment in assignments:
        crew = find_by_id(crews, assignment["crew_id"])
        time_slot = find_by_id(time_slots, assignment["time_slot_id"])
        position = find_by_id(positions, assignment["position_id"])

        crew_name = crew["name"] if crew else "不明なクルー"

        if time_slot:
            time_text = f'{time_slot["start_time"]}-{time_slot["end_time"]}'
        else:
            time_text = "不明な時間帯"

        position_name = position["name"] if position else "不明なポジション"

        print(
            f'{assignment["date"]} | '
            f'{time_text} | '
            f'{position_name} | '
            f'{crew_name}'
        )


print_assignments_readable()