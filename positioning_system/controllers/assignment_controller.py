"""
特定の日付・時間帯・ポジションへの、クルーの配置（Assignment）を
管理するコントローラー。
"""

from models import Assignment
from repositories.assignment_repository import load_assignments, save_assignments


class AssignmentConflictError(Exception):
    """
    同じ日付・時間帯に、同じクルーを別ポジションへ
    重複して配置しようとした場合に送出される。

    以前はエラー時に print() で知らせるだけで、
    呼び出し元（View）がエラーを検知できなかったため、
    例外として送出する形に変更した。
    View側では try/except で受け取り、
    messagebox等でユーザーに通知することを想定している。
    """

    def __init__(self, crew_id: int, date: str, time_slot_id: int):
        self.crew_id = crew_id
        self.date = date
        self.time_slot_id = time_slot_id
        super().__init__(
            f"クルー(id={crew_id})は {date} の時間帯(id={time_slot_id})に"
            "すでに別のポジションへ配置されています"
        )


def _generate_new_id(assignments: list[Assignment]) -> int:
    if not assignments:
        return 1
    return max(assignment.id for assignment in assignments) + 1


def assign_crew_to_position(
    date: str,
    time_slot_id: int,
    position_id: int,
    crew_id: int,
) -> Assignment:
    """
    指定した日付・時間帯・ポジションにクルーを配置する。

    ルール:
    1. 同じ日付・時間帯・ポジションにすでに配置があれば
       クルーを上書きする（配置の変更）
    2. 同じ日付・時間帯に、同じクルーがすでに別ポジションへ
       配置されている場合は AssignmentConflictError を送出する
    """
    assignments = load_assignments()

    for assignment in assignments:
        if (
            assignment.date == date
            and assignment.time_slot_id == time_slot_id
            and assignment.crew_id == crew_id
            and assignment.position_id != position_id
        ):
            raise AssignmentConflictError(crew_id, date, time_slot_id)

    for assignment in assignments:
        if (
            assignment.date == date
            and assignment.time_slot_id == time_slot_id
            and assignment.position_id == position_id
        ):
            assignment.crew_id = crew_id
            save_assignments(assignments)
            return assignment

    new_assignment = Assignment(
        id=_generate_new_id(assignments),
        date=date,
        time_slot_id=time_slot_id,
        position_id=position_id,
        crew_id=crew_id,
    )

    assignments.append(new_assignment)
    save_assignments(assignments)

    return new_assignment


def get_assignments_by_date(date: str) -> list[Assignment]:
    assignments = load_assignments()
    return [a for a in assignments if a.date == date]


def get_assignments_by_date_and_time_slot(
    date: str, time_slot_id: int
) -> list[Assignment]:
    assignments = load_assignments()
    return [
        a for a in assignments
        if a.date == date and a.time_slot_id == time_slot_id
    ]


def get_assignment_by_position(
    date: str, time_slot_id: int, position_id: int
) -> Assignment | None:
    assignments = load_assignments()

    for a in assignments:
        if (
            a.date == date
            and a.time_slot_id == time_slot_id
            and a.position_id == position_id
        ):
            return a

    return None


def delete_assignment(date: str, time_slot_id: int, position_id: int) -> None:
    assignments = load_assignments()

    remaining = [
        a for a in assignments
        if not (
            a.date == date
            and a.time_slot_id == time_slot_id
            and a.position_id == position_id
        )
    ]

    save_assignments(remaining)