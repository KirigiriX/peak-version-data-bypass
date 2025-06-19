import json
from datetime import datetime, timedelta, timezone

FILENAME = "version.json"

with open(FILENAME, "r") as f:
    data = json.load(f)

# datetime aware pour last_updated (en remplaçant le 'Z' par timezone UTC)
last_updated = datetime.fromisoformat(data["LastUpdated"].replace("Z", "+00:00"))

# datetime aware UTC pour now
now = datetime.now(timezone.utc)

# Vérification si au moins 7 minutes sont passées
if (now - last_updated) >= timedelta(minutes=7):
    data["LevelIndex"] += 1
    data["LastUpdated"] = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
    print("LevelIndex mis à jour.")
else:
    print("Pas encore 7 minutes. Pas de mise à jour.")
