from repositories.assignment_repository import load_assignments, save_assignments


def assign_crew_to_position(date, time_slot_id, position_id, crew_id):
    """
    指定した日付・時間帯・ポジションにクルーを配置する。
    すでに同じ日付・時間帯・ポジションの配置がある場合は更新する。
    """

    assignments = load_assignments()

    # すでに同じ枠の配置があるか確認する
    for assignment in assignments:
        if (
            assignment["date"] == date
            and assignment["time_slot_id"] == time_slot_id
            and assignment["position_id"] == position_id
        ):
            assignment["crew_id"] = crew_id
            save_assignments(assignments)
            return assignment

    # なければ新しく追加する
    new_assignment = {
        "id": len(assignments) + 1,
        "date": date,
        "time_slot_id": time_slot_id,
        "position_id": position_id,
        "crew_id": crew_id
    }

    assignments.append(new_assignment)
    save_assignments(assignments)

    return new_assignment


def get_assignments_by_date_and_time_slot(date, time_slot_id):
    """
    指定した日付・時間帯の配置一覧を取得する。
    """

    assignments = load_assignments()

    result = []

    for assignment in assignments:
        if (
            assignment["date"] == date
            and assignment["time_slot_id"] == time_slot_id
        ):
            result.append(assignment)

    return result