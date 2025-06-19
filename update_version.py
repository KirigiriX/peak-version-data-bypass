from datetime import datetime, timedelta, timezone
import json

FILENAME = "version.json"

with open(FILENAME, "r") as f:
    data = json.load(f)

last_updated = datetime.fromisoformat(data["LastUpdated"].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)

minutes = data.get("MinutesUntilLevel", 0)
seconds = data.get("SecondsUntilLevel", 0)
level_index = data.get("LevelIndex", 0)

time_since_update = now - last_updated

# Flag pour savoir si on a fait une mise à jour du LevelIndex
level_updated = False

# Incrémente LevelIndex toutes les 20 minutes
if time_since_update >= timedelta(minutes=20):
    level_index += 1
    # Reset timer à 20 minutes pile
    minutes = 20
    seconds = 0
    last_updated = now
    level_updated = True
    print(f"LevelIndex incremented to {level_index} and timer reset to 20m 0s")

# Sinon, si pas incrémenté, décrémente Minutes/Seconds toutes les 5 minutes
elif time_since_update >= timedelta(minutes=5):
    total_seconds = minutes * 60 + seconds
    total_seconds -= 5 * 60  # décrémente 5 minutes
    if total_seconds < 0:
        total_seconds = 0
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    print(f"Countdown updated: {minutes}m {seconds}s")
else:
    print("Less than 5 minutes since last update. No change.")

# Mise à jour des données
data["MinutesUntilLevel"] = minutes
data["SecondsUntilLevel"] = seconds
data["LevelIndex"] = level_index
data["LastUpdated"] = last_updated.replace(microsecond=0).isoformat().replace("+00:00", "Z")

with open(FILENAME, "w") as f:
    json.dump(data, f, indent=4)
