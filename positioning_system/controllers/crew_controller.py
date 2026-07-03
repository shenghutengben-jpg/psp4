# controllers/crew_controller.py
from repositories.crew_repository import load_crews, save_crews

def get_all_crews():
    return load_crews()

def add_crew(name, start_time, end_time):
    crews = load_crews()

    new_id = 1
    if crews:
        new_id = max(crew["id"] for crew in crews) + 1

    new_crew = {
        "id": new_id,
        "name": name,
        "start_time": start_time,
        "end_time": end_time
    }

    crews.append(new_crew)
    save_crews(crews)

    return new_crew

def delete_crew(crew_id):
    crews = load_crews()
    crews = [crew for crew in crews if crew["id"] != crew_id]
    save_crews(crews)