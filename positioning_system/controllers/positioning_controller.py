from repositories.assignment_repository import load_assignments, save_assignments


def get_new_assignment_id(assignments):
    """
    新しい配置IDを作成する。
    assignments が空なら 1、
    すでにデータがあれば最大ID + 1 にする。
    """

    if not assignments:
        return 1

    return max(assignment["id"] for assignment in assignments) + 1


def assign_crew_to_position(date, time_slot_id, position_id, crew_id):
    """
    指定した日付・時間帯・ポジションにクルーを配置する。

    ルール:
    1. 同じ日付・時間帯・ポジションに配置があれば更新する
    2. 同じ日付・時間帯に同じクルーが別ポジションにいたら配置しない
    """

    assignments = load_assignments()

    # まず、同じ日付・時間帯に同じクルーが別ポジションへ配置されていないか確認
    for assignment in assignments:
        if (
            assignment["date"] == date
            and assignment["time_slot_id"] == time_slot_id
            and assignment["crew_id"] == crew_id
            and assignment["position_id"] != position_id
        ):
            print("エラー: このクルーは同じ時間帯に別のポジションへ配置されています")
            return None

    # すでに同じ枠の配置があるか確認
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
        "id": get_new_assignment_id(assignments),
        "date": date,
        "time_slot_id": time_slot_id,
        "position_id": position_id,
        "crew_id": crew_id
    }

    assignments.append(new_assignment)
    save_assignments(assignments)

    return new_assignment

def get_assignments_by_date(date):
    """
    指定した日付の配置一覧を取得する。
    """

    assignments = load_assignments()

    result = []

    for assignment in assignments:
        if assignment["date"] == date:
            result.append(assignment)

    return result


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


def get_assignment_by_position(date, time_slot_id, position_id):
    """
    指定した日付・時間帯・ポジションの配置を1件取得する。
    見つからなければ None を返す。
    """

    assignments = load_assignments()

    for assignment in assignments:
        if (
            assignment["date"] == date
            and assignment["time_slot_id"] == time_slot_id
            and assignment["position_id"] == position_id
        ):
            return assignment

    return None


def delete_assignment(date, time_slot_id, position_id):
    """
    指定した日付・時間帯・ポジションの配置を削除する。
    """

    assignments = load_assignments()

    new_assignments = []

    for assignment in assignments:
        if (
            assignment["date"] == date
            and assignment["time_slot_id"] == time_slot_id
            and assignment["position_id"] == position_id
        ):
            continue

        new_assignments.append(assignment)

    save_assignments(new_assignments)

    return new_assignments