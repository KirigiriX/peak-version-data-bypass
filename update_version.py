from datetime import datetime, timedelta, timezone
import json

FILENAME = "version.json"

with open(FILENAME, "r") as f:
    data = json.load(f)

# Convert last updated to datetime aware
last_updated = datetime.fromisoformat(data["LastUpdated"].replace("Z", "+00:00"))
now = datetime.now(timezone.utc)

# Check if at least 1 minute passed
if (now - last_updated) >= timedelta(minutes=1):
    # Decrease MinutesUntilLevel by 1
    minutes = data.get("MinutesUntilLevel", 0)
    hours = data.get("HoursUntilLevel", 0)

    if minutes > 0:
        minutes -= 1
    else:
        if hours > 0:
            hours -= 1
            minutes = 59

    data["MinutesUntilLevel"] = minutes
    data["HoursUntilLevel"] = hours
    data["LastUpdated"] = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Countdown updated: {hours}h {minutes}m")
else:
    print("Less than 1 minute since last update. No change.")
