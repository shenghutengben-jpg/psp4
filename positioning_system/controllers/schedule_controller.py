"""
クルーの日ごとの勤務予定（Schedule）を管理するコントローラー。

以前は date_controller.py という名前で、
「日付そのものの管理」と「クルーの勤務登録」という
別々の役割が1ファイルに混在していたため、
役割が伝わりやすいよう schedule_controller に改名した。
（このファイルをimportしている箇所は、次のviews更新時に
 controllers.date_controller → controllers.schedule_controller
 へ書き換える）
"""

from models import Schedule
from repositories.schedule_repository import load_schedules, save_schedules
from controllers.crew_controller import get_or_create_crew


def _generate_new_id(schedules: list[Schedule]) -> int:
    if not schedules:
        return 1
    return max(schedule.id for schedule in schedules) + 1


def add_schedule_by_crew_name(
    date: str,
    crew_name: str,
    start_time: str,
    end_time: str,
) -> Schedule:
    """
    クルー名を指定して勤務予定を登録する。
    同名のクルーが未登録であれば自動的に新規登録する。
    """
    crew = get_or_create_crew(crew_name)

    schedules = load_schedules()

    new_schedule = Schedule(
        id=_generate_new_id(schedules),
        date=date,
        crew_id=crew.id,
        start_time=start_time,
        end_time=end_time,
    )

    schedules.append(new_schedule)
    save_schedules(schedules)

    return new_schedule


def get_schedules_by_date(date: str) -> list[Schedule]:
    schedules = load_schedules()
    return [schedule for schedule in schedules if schedule.date == date]