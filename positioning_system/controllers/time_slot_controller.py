from repositories.time_slot_repository import load_time_slots
from repositories.crew_repository import load_crews
from repositories.schedule_repository import load_schedules


def get_all_time_slots():
    return load_time_slots()


def get_time_slot_by_id(time_slot_id):
    time_slots = load_time_slots()

    for time_slot in time_slots:
        if time_slot["id"] == time_slot_id:
            return time_slot

    return None


# 後回し
def get_previous_time_slot(time_slot_id):
    pass


def get_next_time_slot(time_slot_id):
    pass


def get_crew_by_id(crew_id):
    crews = load_crews()

    for crew in crews:
        if crew["id"] == crew_id:
            return crew

    return None


def is_working_in_time_slot(schedule, time_slot):
    return (
        schedule["start_time"] <= time_slot["start_time"]
        and schedule["end_time"] >= time_slot["end_time"]
    )


def get_working_crews(date, time_slot_id):
    time_slot = get_time_slot_by_id(time_slot_id)

    if not time_slot:
        return []

    schedules = load_schedules()

    working_crews = []

    for schedule in schedules:
        # 日付が違う勤務予定は無視
        if schedule["date"] != date:
            continue

        # その時間帯に勤務しているか判定
        if is_working_in_time_slot(schedule, time_slot):
            crew = get_crew_by_id(schedule["crew_id"])

            if crew is not None:
                working_crews.append(crew)

    return working_crews