from repositories.schedule_repository import load_schedules, save_schedules
from repositories.crew_repository import load_crews, save_crews


def get_or_create_crew(name):
    crews = load_crews()

    for crew in crews:
        if crew["name"] == name:
            return crew

    new_id = 1
    if crews:
        new_id = max(crew["id"] for crew in crews) + 1

    new_crew = {
        "id": new_id,
        "name": name
    }

    crews.append(new_crew)
    save_crews(crews)

    return new_crew


def add_schedule_by_crew_name(date, crew_name, start_time, end_time):
    crew = get_or_create_crew(crew_name)

    schedules = load_schedules()

    new_id = 1
    if schedules:
        new_id = max(schedule["id"] for schedule in schedules) + 1

    new_schedule = {
        "id": new_id,
        "date": date,
        "crew_id": crew["id"],
        "start_time": start_time,
        "end_time": end_time
    }

    schedules.append(new_schedule)
    save_schedules(schedules)

    return new_schedule


def get_schedules_by_date(date):
    schedules = load_schedules()

    result = []

    for schedule in schedules:
        if schedule["date"] == date:
            result.append(schedule)

    return result