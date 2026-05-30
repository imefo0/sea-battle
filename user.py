import json
import os
import sys
import datetime

USERS_DIR = "users"

def add_user(name):
    os.makedirs(USERS_DIR, exist_ok=True)
    path = f"{USERS_DIR}/{name}.json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({"games": []}, f)

def remove_user(name):
    path = f"{USERS_DIR}/{name}.json"
    if os.path.exists(path):
        os.remove(path)

def list_of_users():
    return [f[:-5] for f in os.listdir(USERS_DIR) if f.endswith(".json")]

def add_game(user: str, game: list[list[int]], win: bool) -> bool: # [ [0,0], [1,0] ]
    path = f"{USERS_DIR}/{user}.json"
    if not os.path.exists(path):
        return False
    
    with open(path, "r") as f:
        data = json.load(f)
    
    if data["games"]:
        next_num = data["games"][-1]["num"] + 1
    else:
        next_num = 1

    new_game = {
        "num": next_num,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "shots": game,
        "win": win
    }
    data["games"].append(new_game)
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return True

def info(user: str, num=-1) -> bool:
    path = f"{USERS_DIR}/{user}.json"
    if num == -1: # все игры
        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            data = json.load(f)

        games = data.get("games", [])
        if not games:
            return False

        print(f"{"№":<9}{"Data":<14}{"Status":<6}")
        print("-"*31)

        for i, game in enumerate(games, 1):
            date = game.get("date", "???")
            win = "won" if game.get("win") else "losed"
            print(f"{i:<9}{date:<12}{win:<6}")
    else: # конкретная игра
        pass
    return True

def delete_all_games(user: str) -> bool:
    path = f"{USERS_DIR}/{user}.json"
    if not os.path.exists(path):
        return False
    
    with open(path, "r") as f:
        data = json.load(f)
    
    data["games"] = []  # ← очищаем список
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    
    return True

if __name__ == "__main__":
    cmd = sys.argv[1:]
    if "-c" in cmd:
        os.system("clear")
    if "-n" in cmd:
        add_user(cmd[cmd.index("-n") + 1])
    if "-d" in cmd:
        remove_user(cmd[cmd.index("-d") + 1])
    if "-l" in cmd:
        print(list_of_users())
    if "-r" in cmd:
        delete_all_games(cmd[cmd.index("-r") + 1])

    if "-g" in cmd:
        idx = cmd.index("-g")
        user = cmd[idx + 1]
        shots = json.loads(cmd[idx + 2])
        win = cmd[idx + 3].lower() == "true"
        add_user(user)
        add_game(user, shots, win)
    if "-i" in cmd:
        info(cmd[cmd.index("-i") + 1], int(cmd[cmd.index("-i") + 2]))