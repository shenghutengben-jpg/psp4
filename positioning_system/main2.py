from controllers.positioning_controller import assign_crew_to_position
from controllers.positioning_controller import get_assignments_by_date_and_time_slot
from repositories.assignment_repository import load_assignments


date = "2026-07-03"
time_slot_id = 13
position_id = 1
crew_id = 1


print("=== 配置前 assignments.json ===")
print(load_assignments())


print("\n=== 配置を登録 ===")
assignment = assign_crew_to_position(
    date=date,
    time_slot_id=time_slot_id,
    position_id=position_id,
    crew_id=crew_id
)

print("登録・更新された配置:")
print(assignment)


print("\n=== 配置後 assignments.json ===")
print(load_assignments())


print("\n=== 指定した日付・時間帯の配置一覧 ===")
assignments = get_assignments_by_date_and_time_slot(date, time_slot_id)
print(assignments)