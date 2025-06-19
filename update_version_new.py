from datetime import datetime, timedelta, timezone
import json, pathlib

FILENAME = pathlib.Path("version.json")

with FILENAME.open() as f:
    data = json.load(f)

now = datetime.now(timezone.utc)
level   = data.get("LevelIndex", 0)
remain  = timedelta(
    minutes=data.get("MinutesUntilLevel", 20),
    seconds=data.get("SecondsUntilLevel", 0)
)

# une exécution -> 5 min écoulées
remain -= timedelta(minutes=5)

# quand le ça passe à zéro:
while remain <= timedelta():
    level  += 1
    remain += timedelta(minutes=20)

# sauvegarder juste si quelque chose a changé
if (level != data["LevelIndex"] or
    remain.seconds//60 != data["MinutesUntilLevel"] or
    remain.seconds%60  != data["SecondsUntilLevel"]):

    data.update({
        "LevelIndex":          level,
        "MinutesUntilLevel":   remain.seconds // 60,
        "SecondsUntilLevel":   remain.seconds % 60,
        "LastUpdated":         now.replace(microsecond=0).isoformat().replace("+00:00","Z")
    })
    with FILENAME.open("w") as f:
        json.dump(data, f, indent=4)
