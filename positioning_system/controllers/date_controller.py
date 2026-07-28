import re
from repositories.schedule_repository import load_schedules, save_schedules
from repositories.crew_repository import load_crews, save_crews

def time_to_minutes(time_text):
    """
    '12:00' のような時刻文字列を分に変換する。
    00:00〜24:00 まで許可する。
    """

    if not re.match(r"^\d{2}:\d{2}$", time_text):
        raise ValueError("時刻は 12:00 のように入力してください")

    hour, minute = map(int, time_text.split(":"))

    if hour < 0 or hour > 24:
        raise ValueError("時は 00〜24 の範囲で入力してください")

    if minute < 0 or minute >= 60:
        raise ValueError("分は 00〜59 の範囲で入力してください")

    if hour == 24 and minute != 0:
        raise ValueError("24時台は 24:00 のみ入力できます")

    return hour * 60 + minute


def validate_work_time(start_time, end_time):
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    if start_minutes >= end_minutes:
        raise ValueError("出勤時間は退勤時間より前にしてください")

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
    validate_work_time(start_time, end_time)

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

def time_to_minutes(time_text):
    """
    '12:00' のような時刻文字列を分に変換する。
    00:00〜24:00 まで許可する。
    """

    if not re.match(r"^\d{2}:\d{2}$", time_text):
        raise ValueError("時刻は 12:00 のように入力してください")

    hour, minute = map(int, time_text.split(":"))

    if hour < 0 or hour > 24:
        raise ValueError("時は 00〜24 の範囲で入力してください")

    if minute < 0 or minute >= 60:
        raise ValueError("分は 00〜59 の範囲で入力してください")

    if hour == 24 and minute != 0:
        raise ValueError("24時台は 24:00 のみ入力できます")

    return hour * 60 + minute


def validate_work_time(start_time, end_time):
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    if start_minutes >= end_minutes:
        raise ValueError("出勤時間は退勤時間より前にしてください")
    
def update_schedule(schedule_id, crew_name, start_time, end_time):
    """
    指定した schedule_id の勤務予定を編集する。
    クルー名が未登録なら crews.json に追加し、その crew_id を使う。
    """

    validate_work_time(start_time, end_time)

    schedules = load_schedules()
    crew = get_or_create_crew(crew_name)

    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedule["crew_id"] = crew["id"]
            schedule["start_time"] = start_time
            schedule["end_time"] = end_time

            save_schedules(schedules)
            return schedule

    return None


def delete_schedule(schedule_id):
    """
    指定した schedule_id の勤務予定を削除する。
    """

    schedules = load_schedules()

    new_schedules = []

    for schedule in schedules:
        if schedule["id"] != schedule_id:
            new_schedules.append(schedule)

    save_schedules(new_schedules)

    return new_schedules