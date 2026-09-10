import csv


def load_csv(path):

    with open(path, newline='') as file:

        reader = csv.DictReader(file)

        return list(reader)



def load_spells():
    spells = {}

    with open("database/game_data/spells.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            spell_id = int(row["id"])

            spells[spell_id] = {
                "id": spell_id,
                "name": row["name"],
                "effect": row["effect"],
                "damage": int(row["damage"]),
                "mana": int(row["mana"]),
                "animation_id": row["animation_id"]
            }

    return spells