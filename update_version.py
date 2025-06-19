import time
import json

# Chemin vers ton fichier existant
json_file = "version.json"

def load_data():
    with open(json_file, "r") as f:
        return json.load(f)

def save_data(data):
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

def display(data):
    print(f"Level: {data['LevelIndex']} | Temps restant: {data['MinutesUntilLevel']:02}:{data['SecondsUntilLevel']:02}")

def reset_timer(data):
    data["MinutesUntilLevel"] = 20
    data["SecondsUntilLevel"] = 0

# Boucle principale
while True:
    data = load_data()
    display(data)

    time.sleep(1)

    if data["SecondsUntilLevel"] == 0:
        if data["MinutesUntilLevel"] == 0:
            # Niveau atteint
            data["LevelIndex"] += 1
            reset_timer(data)
        else:
            data["MinutesUntilLevel"] -= 1
            data["SecondsUntilLevel"] = 59
    else:
        data["SecondsUntilLevel"] -= 1

    save_data(data)
