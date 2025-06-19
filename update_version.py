from datetime import datetime, timedelta, timezone
import json

FILENAME = "version.json"

with open(FILENAME, "r") as f:
    data = json.load(f)

last_updated = datetime.fromisoformat(data["LastUpdated"].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)

minutes = data.get("MinutesUntilLevel", 20)
seconds = data.get("SecondsUntilLevel", 0)
level_index = data.get("LevelIndex", 0)

time_since_update = now - last_updated

# Flag pour savoir si on a fait une mise à jour du LevelIndex ou du timer
data_updated = False

# Incrémente LevelIndex toutes les 20 minutes pile
if time_since_update >= timedelta(minutes=20):
    level_index += 1
    minutes = 20
    seconds = 0
    last_updated = now
    data_updated = True
    print(f"LevelIndex incremented to {level_index} and timer reset to 20m 0s")

# Sinon, si pas incrémenté, décrémente Minutes/Seconds toutes les 5 minutes
elif time_since_update >= timedelta(minutes=3):
    total_seconds = minutes * 60 + seconds
    total_seconds -= 5 * 60  # décrémente 5 minutes

    if total_seconds < 0:
        total_seconds = 0

    new_minutes = total_seconds // 60
    new_seconds = total_seconds % 60

    if new_minutes != minutes or new_seconds != seconds:
        minutes = new_minutes
        seconds = new_seconds
        last_updated = now
        data_updated = True
        print(f"Countdown updated: {minutes}m {seconds}s")
    else:
        print("Countdown already at 0m 0s, no change.")

else:
    print("Less than 5 minutes since last update. No change.")

# Mise à jour des données si nécessaire
if data_updated:
    data["MinutesUntilLevel"] = minutes
    data["SecondsUntilLevel"] = seconds
    data["LevelIndex"] = level_index
    data["LastUpdated"] = last_updated.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
else:
    print("No data update, skipping file write.")
