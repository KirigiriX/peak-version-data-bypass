import time
import json
import os

SAVE_FILE = "version.json"
LEVEL_UP_TOTAL_MINUTES = 60
MESSAGE_CHANGE_SECONDS = 1200
MESSAGES = [
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

def get_default_data():
    hours, minutes = divmod(LEVEL_UP_TOTAL_MINUTES, 60)
    return {
        "VersionOkay": True,
        "HoursUntilLevel": hours,
        "MinutesUntilLevel": minutes,
        "SecondsUntilLevel": 0,
        "LevelIndex": 1,
        "Message": MESSAGES[0],
        "MessageIndex": 0
    }

def load_data():
    if not os.path.exists(SAVE_FILE):
        return get_default_data()
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        if 'MessageIndex' not in data:
            try:
                data['MessageIndex'] = MESSAGES.index(data['Message'])
            except ValueError:
                data['MessageIndex'] = 0
        return data
    except (json.JSONDecodeError, IOError):
        print("Error reading save file. Using default data.")
        return get_default_data()

def save_data(data):
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

def display(data):
    print(
        f"\rLevel: {data['LevelIndex']} | "
        f"Time Left: {data.get('HoursUntilLevel', 0):02}:{data['MinutesUntilLevel']:02}:{data['SecondsUntilLevel']:02} | "
        f"Message: {data['Message']}",
        end=""
    )

def reset_timer(data):
    hours, minutes = divmod(LEVEL_UP_TOTAL_MINUTES, 60)
    data["HoursUntilLevel"] = hours
    data["MinutesUntilLevel"] = minutes
    data["SecondsUntilLevel"] = 0

def main():
    data = load_data()
    message_timer = 0
    try:
        while True:
            display(data)
            time.sleep(1)
            data['SecondsUntilLevel'] -= 1
            if data['SecondsUntilLevel'] < 0:
                data['SecondsUntilLevel'] = 59
                data['MinutesUntilLevel'] -= 1
                if data['MinutesUntilLevel'] < 0:
                    data['MinutesUntilLevel'] = 59
                    data['HoursUntilLevel'] = data.get('HoursUntilLevel', 1) - 1
            if data.get('HoursUntilLevel', 0) < 0:
                data['LevelIndex'] += 1
                reset_timer(data)
                print(f"\Reached level {data['LevelIndex']}.")
            message_timer += 1
            if message_timer >= MESSAGE_CHANGE_SECONDS:
                new_index = (data.get('MessageIndex', 0) + 1) % len(MESSAGES)
                data['MessageIndex'] = new_index
                data['Message'] = MESSAGES[new_index]
                message_timer = 0
            save_data(data)
    except KeyboardInterrupt:
        print("\n\nExiting. Saving final state...")
        save_data(data)

if __name__ == "__main__":
    main()
