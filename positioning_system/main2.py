from controllers.positioning_controller import assign_crew_to_position
from controllers.positioning_controller import get_assignments_by_date_and_time_slot

assign_crew_to_position("2026-07-03", 4, 1, 2)

assignments = get_assignments_by_date_and_time_slot("2026-07-03", 4)

print(assignments)