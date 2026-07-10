from repositories.schedule_repository import load_schedules


def get_schedules_by_date(date):
    schedules = load_schedules()

    result = []

    for schedule in schedules:
        if schedule["date"] == date:
            result.append(schedule)

    return result