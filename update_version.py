import json

file_path = "version.json"

# Charger le fichier
with open(file_path, "r") as f:
    data = json.load(f)

minutes = data["MinutesUntilLevel"]
seconds = data["SecondsUntilLevel"]

if minutes == 0 and seconds == 0:
    # Temps écoulé : monter de niveau
    data["LevelIndex"] += 1
    data["MinutesUntilLevel"] = 20
    data["SecondsUntilLevel"] = 0
else:
    # Décrémentation normale
    if seconds == 0:
        data["MinutesUntilLevel"] -= 1
        data["SecondsUntilLevel"] = 59
    else:
        data["SecondsUntilLevel"] -= 1

# Sauvegarder
with open(file_path, "w") as f:
    json.dump(data, f, indent=4)
