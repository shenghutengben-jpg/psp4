from repositories.crew_repository import load_crews, save_crews


def get_all_crews():
    return load_crews()


def get_crew_by_id(crew_id):
    crews = load_crews()

    for crew in crews:
        if crew["id"] == crew_id:
            return crew

    return None


def add_crew(name):
    crews = load_crews()

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


def delete_crew(crew_id):
    crews = load_crews()

    new_crews = []
    for crew in crews:
        if crew["id"] != crew_id:
            new_crews.append(crew)

    save_crews(new_crews)