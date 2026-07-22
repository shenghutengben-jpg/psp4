"""
時間帯（TimeSlot）に関する処理と、
「特定の日付・時間帯に出勤しているクルー一覧」を取得する処理を担当する
コントローラー。

get_crew_by_id は crew_controller に一本化したため、
ここでは crew_controller のものをそのまま利用する
（以前は同じ実装がここにも重複していた）。
"""

from models import TimeSlot
from repositories.time_slot_repository import load_time_slots
from repositories.schedule_repository import load_schedules
from controllers.crew_controller import get_crew_by_id


def get_all_time_slots() -> list[TimeSlot]:
    """
    開始時刻順に並べ替えた時間帯一覧を返す。
    前後の時間帯を求める処理(get_previous_time_slot等)がこの並び順に
    依存しているため、常にソート済みの状態で返す。
    """
    time_slots = load_time_slots()
    return sorted(time_slots, key=lambda ts: ts.start_time)


def get_time_slot_by_id(time_slot_id: int) -> TimeSlot | None:
    for time_slot in get_all_time_slots():
        if time_slot.id == time_slot_id:
            return time_slot

    return None


def get_previous_time_slot(time_slot_id: int) -> TimeSlot | None:
    """
    指定した時間帯の一つ前の時間帯を返す。
    最初の時間帯の場合や、該当IDが存在しない場合は None を返す。
    """
    time_slots = get_all_time_slots()

    for index, time_slot in enumerate(time_slots):
        if time_slot.id == time_slot_id:
            if index == 0:
                return None
            return time_slots[index - 1]

    return None


def get_next_time_slot(time_slot_id: int) -> TimeSlot | None:
    """
    指定した時間帯の一つ後の時間帯を返す。
    最後の時間帯の場合や、該当IDが存在しない場合は None を返す。
    """
    time_slots = get_all_time_slots()

    for index, time_slot in enumerate(time_slots):
        if time_slot.id == time_slot_id:
            if index == len(time_slots) - 1:
                return None
            return time_slots[index + 1]

    return None


def is_working_in_time_slot(schedule, time_slot: TimeSlot) -> bool:
    """
    あるクルーの勤務予定(schedule)が、指定した時間帯(time_slot)を
    完全にカバーしているかどうかを判定する。

    以前は position_edit_view.py 側にも文字列比較による
    同様の判定ロジックが存在していたため、ここに一本化した。
    Viewからは get_working_crews の結果を使うだけにする。
    """
    return (
        schedule.start_time <= time_slot.start_time
        and schedule.end_time >= time_slot.end_time
    )


def get_working_crews(date: str, time_slot_id: int) -> list:
    """
    指定した日付・時間帯に出勤しているクルー一覧を返す。
    """
    time_slot = get_time_slot_by_id(time_slot_id)

    if time_slot is None:
        return []

    schedules = load_schedules()

    working_crews = []

    for schedule in schedules:
        if schedule.date != date:
            continue

        if is_working_in_time_slot(schedule, time_slot):
            crew = get_crew_by_id(schedule.crew_id)

            if crew is not None:
                working_crews.append(crew)

    return working_crews