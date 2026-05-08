import time
import os
import random
import bot

true = True
false = False

player_field = []
player_radar = []
bot_field = []
bot_radar = []

field = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
emoji = ["🌊", "🚢", "🌊", "🔹", "💥", "💀"]
""" 0 - скрытый корабль 🌊, 
1 - открытый корабль 🚢, 
2 - скрытая пустышка 🌊, 
3 - открытая пустышка 🔸, 
4 - попал 💥
5 - убит 💀

когда атака в:
0 -> 4
2 -> 3
1 - после игры/при расстановке кораблей
5 - когда весь корабль убит
"""

def clear():
    os.system("clear")

def translate_to_emoji(num):
    return emoji[num]

def translate_from_word(word):
    words = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
    return words.index(word.capitalize())

def translate_to_num(list):
    return f"{''.join(map(str, list))}"

def create_field():
    return [[2 for _ in range(10)] for _ in range(10)]

def print_field(field):
    words = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]

    print(end="   ")
    for i in words:
        print(i, end="  ")
    print()

    for i in range(len(field)):
        print(f" {i+1}" if i != 9 else f"{i+1}", end=" ")
        for j in field[i]:
            print(translate_to_emoji(j), end=" ")
        print()

def change_cell(cell_plus_num):
    field[int(cell_plus_num[1])][
        int(cell_plus_num[0])] = int(cell_plus_num[2])

def randomize():
    for i in range(len(field)):
        for j in field[i]:
            field[random.randint(0, 9)][
                random.randint(0, 9)] = random.choice([0, 2])

def fire(cell):
    x = int(cell[0])
    y = int(cell[1])
    if field[y][x] == 0:
        field[y][x] = 4
    elif field[y][x] == 2:
        field[y][x] = 3

def set_ship_OLD(a, b):
    ya = translate_from_word(a[0])
    yb = translate_from_word(b[0])
    xa = int(a[1]) - 1
    xb = int(b[1]) - 1
    maxx = max(xa, xb)
    minx = min(xa, xb)
    maxy = max(ya, yb)
    miny = min(ya, yb)
    if xa == xb and maxy - miny <= 3:
        for i in range(miny, maxy+1):
            change_cell(f"{i}{xa}1")
    elif ya == yb and maxx - minx <= 3:
        for i in range(minx, maxx+1):
            change_cell(f"{i}{ya}1")
    else:
        print("NO")
        return
    
def set_ship_1():
    pass

def set_ship_2(coordinate, direction, num: int, is_player: bool):
    x = int(coordinate[0])
    y = int(coordinate[1])
    d = direction
    
    try:
        match d:
            case ">":
                if x + num > 10: raise IndexError() 
            case "<":
                if x - num < 1: raise IndexError() 
            case "^":
                if y - num < 10: raise IndexError()
            case "v":
                if y + num > 1: raise IndexError()
            case _: raise IndexError() 

        for n in range(num): #исправить, убрать цикл, делать как x+n 
            change_cell(f"{x}{y}{1}")
            if d == ">": x += 1
            elif d == "<": x -= 1
            elif d == "^": y -= 1
            elif d == "v": y += 1
            else: raise IndexError() 
    
    # добавить механику добавления корабля в список 
    # ships_player/bot_has
        
    except IndexError:
        print("It is impossible to place the ship in this way")

def bot_move(bot_name):
    if bot_name in ["greenhorn", "random", "1"]:
        fire(translate_to_num(bot.greenhorn(field)))

    elif bot_name in ["harpooner", "hunter", "2"]:
        pass

    elif bot_name in ["navigator", "chessman", "3"]:
        pass
    
    elif bot_name in ["admiral", "heat", "4"]:
        pass
    
    elif bot_name in ["master seawolf", "heat+history", "5"]:
        pass
    
    else:
        pass

def player_move():
    pass

# нормально сделать чтобы корды были везде через [x, y], 
# а не как попало