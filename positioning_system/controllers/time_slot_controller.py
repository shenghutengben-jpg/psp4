from repositories.time_slot_repository import load_time_slots
from repositories.crew_repository import load_crews

def get_all_time_slots():
    # repositoryから時間帯一覧を取得する
    return load_time_slots()

def get_time_slot_by_id(time_slot_id):
    time_slots = load_time_slots()
    for time_slot in time_slots:
        if time_slot["id"] == time_slot_id:
            return time_slot
    return None

#後回し
def get_previous_time_slot(time_slot_id):
    pass

def get_next_time_slot(time_slot_id):
    pass

def is_working_in_time_slot(crew, time_slot):
    return (
        crew["start_time"] <= time_slot["start_time"]
        and crew["end_time"] >= time_slot["end_time"]
    )

def get_working_crews(time_slot_id):
    time_slot = get_time_slot_by_id(time_slot_id)
    if not time_slot:
        return []
    crews = load_crews()
    working_crews = [crew for crew in crews if is_working_in_time_slot(crew, time_slot)]
    return working_crews
