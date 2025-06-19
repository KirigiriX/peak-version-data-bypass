import json
from datetime import datetime, timedelta
import os

FILENAME = "version.json"

with open(FILENAME, "r") as f:
    data = json.load(f)

last_updated = datetime.fromisoformat(data["LastUpdated"].replace("Z", "+00:00"))
now = datetime.utcnow()

# Si plus de 24h sont passées
if (now - last_updated) >= timedelta(minutes=7):
    data["LevelIndex"] += 1
    data["LastUpdated"] = now.replace(microsecond=0).isoformat() + "Z"

    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
    print("LevelIndex mis à jour.")
else:
    print("Pas encore 7 minutes. Pas de mise à jour.")