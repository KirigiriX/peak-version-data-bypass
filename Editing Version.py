import time
import json

json_file = "version.json"

messages = [
    "Made with love by Kirigiri",
    "You're amazing, keep it up",
    "A little moment of softness",
    "Every second brings you closer to success",
    "You even light up lines of code",
    "Stay kind. Stay strong. Stay you",
    "Small steps lead to big things",
    "You're braver than you think",
    "A virtual cookie just for you",
    "Smile! You're doing your best",
    "One small step for you, one big step for your level",
    "You're never alone, even the code is with you",
    "You're making the world prettier, pixel by pixel",
    "Kindness, motivation, and a touch of magic",
    "You're the cherry on top",
    "A world without bugs... thanks to you",
    "Every click is a victory",
    "Keep going, little hero of code",
    "Don't forget to breathe",
    "Your kindness is your superpower"
]

def load_data():
    with open(json_file, "r") as f:
        return json.load(f)

def save_data(data):
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

def display(data):
    print(f"Level: {data['LevelIndex']} | Temps restant: {data['MinutesUntilLevel']:02}:{data['SecondsUntilLevel']:02} | Message: {data['Message']}")

def reset_timer(data):
    data["MinutesUntilLevel"] = 60
    data["SecondsUntilLevel"] = 0

seconds_since_last_message_change = 0
message_index = 0

while True:
    data = load_data()
    display(data)

    time.sleep(1)

    if data["SecondsUntilLevel"] == 0:
        if data["MinutesUntilLevel"] == 0:
            data["LevelIndex"] += 1
            reset_timer(data)
        else:
            data["MinutesUntilLevel"] -= 1
            data["SecondsUntilLevel"] = 59
    else:
        data["SecondsUntilLevel"] -= 1

    seconds_since_last_message_change += 1
    if seconds_since_last_message_change >= 1200:
        message_index = (message_index + 1) % len(messages)
        data["Message"] = messages[message_index]
        seconds_since_last_message_change = 0

    save_data(data)
